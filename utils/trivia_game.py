import asyncio
import random
import re
from typing import Dict, List
from collections import defaultdict
import discord

class TriviaGame:
    def __init__(self, bot, channel, topic):
        self.bot = bot
        self.channel = channel
        self.topic = topic
        self.players: Dict[int, int] = defaultdict(int)  # User ID: Score
        self.current_question = None
        self.current_answer = None
        self.current_options = []
        self.question_count = 0
        self.max_questions = 5
        self.asked_questions: List[str] = []  # To keep track of asked questions
        self.answer_timeout = 15.0  # Seconds to wait for answers
        self.is_active = True

    async def generate_question(self):
        attempts = 5  # Increase attempts to allow for more variety
        for attempt in range(attempts):
            prompt = (
                f"Generate a multiple choice trivia question about {self.topic}. "
                f"This is question number {self.question_count + 1} out of {self.max_questions}. "
                "Make sure it's different from these previously asked questions: "
                f"{', '.join(self.asked_questions)}. "
                "Provide the question, four options (A, B, C, D), and the correct answer letter in the following format:\n"
                "Question: [Your question here]\n"
                "A: [Option A]\n"
                "B: [Option B]\n"
                "C: [Option C]\n"
                "D: [Option D]\n"
                "Answer: [Correct answer letter]"
            )
            response = await self.bot.generate_response([{"role": "user", "content": prompt}])
            
            # Use regex to extract question, options, and answer
            match = re.search(r"Question: (.*?)\nA: (.*?)\nB: (.*?)\nC: (.*?)\nD: (.*?)\nAnswer: (.)", response, re.DOTALL)
            if match:
                question, optionA, optionB, optionC, optionD, answer = match.groups()
                question = question.strip()
                options = [optionA.strip(), optionB.strip(), optionC.strip(), optionD.strip()]
                answer = answer.strip().upper()
                
                # Check if this question is unique
                if question not in self.asked_questions:
                    self.asked_questions.append(question)
                    return question, options, answer
        
        # If we couldn't generate a unique question after several attempts, raise an exception
        raise ValueError(f"Failed to generate a unique question about {self.topic} after {attempts} attempts.")

    async def wait_for_answers(self):
        answered_players = set()
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < self.answer_timeout and self.is_active:
            try:
                message = await self.bot.wait_for(
                    'message',
                    timeout=self.answer_timeout - (asyncio.get_event_loop().time() - start_time),
                    check=lambda m: m.channel == self.channel and not m.author.bot
                )
                
                if message.content.lower() == '!stop_trivia' and message.author.guild_permissions.administrator:
                    self.is_active = False
                    await self.channel.send("Trivia game stopped by an administrator.")
                    return

                if message.author.id not in answered_players:
                    answered_players.add(message.author.id)
                    if message.content.upper() == self.current_answer:
                        await self.channel.send(f"Correct, {message.author.mention}!")
                        self.players[message.author.id] += 1
                    elif message.content.upper() in ['A', 'B', 'C', 'D']:
                        await self.channel.send(f"Sorry {message.author.mention}, that's incorrect.")
                    else:
                        await self.channel.send(f"{message.author.mention}, please answer with A, B, C, or D.")

            except asyncio.TimeoutError:
                break

        if self.is_active:
            await self.channel.send(f"Time's up! The correct answer was: {self.current_answer}")

    async def start_game(self):
        await self.channel.send(f"Starting a trivia game on the topic of {self.topic}! Get ready!")
        await asyncio.sleep(2)

        while self.question_count < self.max_questions and self.is_active:
            self.question_count += 1
            try:
                self.current_question, self.current_options, self.current_answer = await self.generate_question()
            except ValueError as e:
                await self.channel.send(f"Error generating question: {str(e)}")
                continue

            question_text = f"Question {self.question_count}: {self.current_question}\n"
            for i, option in enumerate(['A', 'B', 'C', 'D']):
                question_text += f"{option}: {self.current_options[i]}\n"
            
            await self.channel.send(question_text)
            await self.wait_for_answers()
            if self.is_active:
                await asyncio.sleep(2)

        if self.is_active:
            await self.end_game()

    async def end_game(self):
        if not self.players:
            await self.channel.send("The trivia game has ended. No one scored any points!")
        else:
            winner = max(self.players, key=self.players.get)
            winner_user = self.channel.guild.get_member(winner)
            await self.channel.send(f"The trivia game has ended! The winner is {winner_user.mention} with {self.players[winner]} points!")

        # Create a summary of the final scores
        sorted_players = sorted(self.players.items(), key=lambda x: x[1], reverse=True)
        summary = "Final Scores:\n"
        for player_id, score in sorted_players:
            player = self.channel.guild.get_member(player_id)
            if player:
                summary += f"{player.name}: {score} point{'s' if score != 1 else ''}\n"

        # Add some statistics
        total_questions = self.question_count
        total_players = len(self.players)
        average_score = sum(self.players.values()) / total_players if total_players > 0 else 0

        summary += f"\nGame Statistics:\n"
        summary += f"Total Questions: {total_questions}\n"
        summary += f"Total Players: {total_players}\n"
        summary += f"Average Score: {average_score:.2f}\n"

        await self.channel.send(summary)

# Global dictionary to store active games
active_games = {}