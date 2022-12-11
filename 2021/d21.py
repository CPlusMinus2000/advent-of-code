import argparse as ap
import re
import sys
import functools

from collections import defaultdict
from copy import copy


DISTRIBUTION = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

WIN_SCORE_P2 = 21

class Track:
    def __init__(self, p1: int, p2: int):
        self.p1 = p1 - 1
        self.p2 = p2 - 1
        self.length = 10
    
    def __str__(self) -> str:
        return f"{self.p1 + 1}/{self.p2 + 1}"
    
    def __repr__(self) -> str:
        return f"Track({self.p1 + 1}, {self.p2 + 1})"
    
    def __getitem__(self, item: int):
        if not isinstance(item, int) or item not in [0, 1]:
            raise ValueError("Track indices must be 0 or 1.")
        
        if item == 0:
            return self.p1
        else:
            return self.p2
    
    def __setitem__(self, key: int, value: int):
        if not isinstance(key, int) or key not in [0, 1]:
            raise ValueError("Track indices must be 0 or 1.")
        
        if key == 0:
            self.p1 = value
        else:
            self.p2 = value
    
    def __hash__(self) -> int:
        return hash((self.p1, self.p2))
    
    def __copy__(self) -> "Track":
        return Track(self.p1 + 1, self.p2 + 1)
    
    def advance_player(self, player: int, moves: int) -> int:
        if not isinstance(player, int) or player not in [0, 1]:
            raise ValueError("Player indices must be 0 or 1.")

        if not isinstance(moves, int):
            raise ValueError("Moves must be an integer.")

        pos = (self[player] + moves) % self.length
        self[player] = pos
        return self[player] + 1

class State:
    """
    A possible Dirac Dice game state.
    """

    def __init__(
        self,
        turn: int,
        pos_one: int,
        pos_two: int,
        score_one: int,
        score_two: int
    ):
        self.turn = turn
        self.pos_one = pos_one
        self.pos_two = pos_two
        self.score_one = score_one
        self.score_two = score_two
    
    def __str__(self) -> str:
        return f"{self.turn + 1}/{self.pos_one + 1}/{self.pos_two + 1}/{self.score_one}/{self.score_two}"
    
    def __repr__(self) -> str:
        return f"State({self.turn + 1}, {self.pos_one + 1}, {self.pos_two + 1}, {self.score_one}, {self.score_two})"
    
    def __hash__(self) -> int:
        return hash((self.turn, self.pos_one, self.pos_two, self.score_one, self.score_two))


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()
        
        self.lines = self.input.splitlines()
        self.p1, self.p2 = int(self.lines[0][-1]), int(self.lines[1][-1])
        self.track = Track(self.p1, self.p2)
        self.score_one = 0
        self.score_two = 0
        self.die = 0
    
    def roll(self) -> int:
        self.die += 1
        return self.die

    def solve_part1(self) -> int:
        while self.score_one < 1000 and self.score_two < 1000:
            n = self.roll() + self.roll() + self.roll()
            self.score_one += self.track.advance_player(0, n)

            if self.score_one >= 1000:
                break
        
            n = self.roll() + self.roll() + self.roll()
            self.score_two += self.track.advance_player(1, n)
        
        return min(self.score_one, self.score_two) * self.die

    def solve_part2(self) -> int:
        p1_wins = 0
        p2_wins = 0
        states = defaultdict(int)
        states[State(0, self.p1, self.p2, 0, 0)] = 1

        while states:
            states_copy = copy(states)
            print(len(states))
            for state in states:
                current_turn = state.turn

                for res in DISTRIBUTION:
                    p1_score = state.score_one
                    p2_score = state.score_two
                    p1_pos = state.pos_one
                    p2_pos = state.pos_two

                    if current_turn == 0:
                        p1_pos = 10 if (p1_pos + res) % 10 == 0 else (p1_pos + res) % 10
                        p1_score += p1_pos
                    else:
                        p2_pos = 10 if (p2_pos + res) % 10 == 0 else (p2_pos + res) % 10
                        p2_score += p2_pos
                    
                    states_copy[State(
                        1 - current_turn,
                        p1_pos,
                        p2_pos,
                        p1_score,
                        p2_score
                    )] += DISTRIBUTION[res] * states[state]

                states_copy[state] -= states[state]
            
            states = states_copy
            for state in states.copy():
                if state.score_one >= WIN_SCORE_P2 or states[state] == 0:
                    p1_wins += states[state]
                    del states[state]
                elif state.score_two >= WIN_SCORE_P2 or states[state] == 0:
                    p2_wins += states[state]
                    del states[state]
        
        return max(p1_wins, p2_wins)
    
    def solve_part2_better(self) -> int:
        states = defaultdict(int)
        states[State(0, self.p1, self.p2, 0, 0)] = 1

        for _ in range(40):
            states_copy = copy(states)
            print(len(states))
            for state in states:
                if state.score_one >= WIN_SCORE_P2 or state.score_two >= WIN_SCORE_P2:
                    continue

                current_turn = state.turn

                for res in DISTRIBUTION:
                    p1_score = state.score_one
                    p2_score = state.score_two
                    p1_pos = state.pos_one
                    p2_pos = state.pos_two

                    if current_turn == 0:
                        p1_pos = 10 if (p1_pos + res) % 10 == 0 else (p1_pos + res) % 10
                        p1_score += p1_pos
                    else:
                        p2_pos = 10 if (p2_pos + res) % 10 == 0 else (p2_pos + res) % 10
                        p2_score += p2_pos

                    states_copy[State(
                        1 - current_turn,
                        p1_pos,
                        p2_pos,
                        p1_score,
                        p2_score
                    )] += DISTRIBUTION[res] * states[state]

                states_copy[state] -= states[state]
            
            states = states_copy
        
        p1_wins = sum(states[state] for state in states if state.score_one >= WIN_SCORE_P2)
        p2_wins = sum(states[state] for state in states if state.score_two >= WIN_SCORE_P2)
        return max(p1_wins, p2_wins)

    @functools.cache    
    def solve_part2_faster(
        self,
        p1_pos,
        p2_pos,
        p1_score,
        p2_score
    ) -> int:
        if p2_score >= WIN_SCORE_P2:
            return 0, 1
        
        wins1, wins2 = 0, 0
        for res, outcomes in DISTRIBUTION.items():
            # p1_pos_ = 10 if (p1_pos + res) % 10 == 0 else (p1_pos + res) % 10
            p1_pos_ = (p1_pos + res) % 10 or 10
            w2, w1 = self.solve_part2_faster(
                p2_pos, p1_pos_, p2_score, p1_score + p1_pos_
            )

            wins1 += outcomes * w1
            wins2 += outcomes * w2
        
        return wins1, wins2
    
    def use_solve_part2_faster(self) -> int:
        return max(self.solve_part2_faster(self.p1, self.p2, 0, 0))


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    parser.add_argument(
        "win_score", type=int, nargs='?', default=21,
        help="Win score for part 2"
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"

    WIN_SCORE_P2 = args.win_score
    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    # print(f"Part 2: {sol.solve_part2_better()}")
    print(f"Part 2: {sol.use_solve_part2_faster()}")
