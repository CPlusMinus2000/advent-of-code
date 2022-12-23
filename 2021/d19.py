import argparse as ap
import re
import sys
import itertools as it

from typing import List, Iterator, Dict, Set
from collections import deque
from point import Point3D


class Scanner:
    def __init__(self, beacons: List[Point3D]):
        self.beacons = beacons
        self.location = Point3D(0, 0, 0)

    def __contains__(self, point: Point3D) -> bool:
        return point in self.beacons

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.beacons)

    def __len__(self) -> int:
        return len(self.beacons)

    def __getitem__(self, index: int) -> Point3D:
        return self.beacons[index]

    def rotate(self, rotation: int) -> "Scanner":
        return Scanner([point.rotate(rotation) for point in self])

    def translate(self, translation: Point3D) -> None:
        self.location += translation
        self.beacons = [b + translation for b in self.beacons]

    def in_range(self, point: Point3D) -> bool:
        """
        Checks if a point is in range of this scanner.
        """

        if not isinstance(point, Point3D):
            raise TypeError("Can't check if non-point is in range of scanner")

        return (
            abs(point.x - self.location.x) <= 500
            and abs(point.y - self.location.y) <= 500
            and abs(point.z - self.location.z) <= 500
        )

    def dists(self) -> Dict[Point3D, List[Point3D]]:
        """
        Return a dictionary of all possible distances between
        one beacon and all other beacons.
        """

        return {
            beacon: {
                other - beacon for other in self.beacons
                if other is not beacon
            } for beacon in self.beacons
        }

    def compare_dists(self, other: "Scanner") -> Set[Point3D]:
        """
        Compares the dists between two scanners, finding the maximum
        amount of identical distances and returning that as a score.
        """

        beacon_info = (0, 0)
        max_intersect = set()
        self_dists = self.dists()
        other_dists = other.dists()
        for s_beacon in self.beacons:
            for other_beacon in other.beacons:
                intersect = self_dists[s_beacon] & other_dists[other_beacon]
                if len(intersect) > len(max_intersect):
                    max_intersect = intersect
                    beacon_info = s_beacon, other_beacon

        return *beacon_info, max_intersect


class Solution:
    def __init__(self, filename: str):
        with open(filename, "r") as f:
            self.input = f.read()

        self.scanners = []
        for scanner in self.input.split("\n\n"):
            scanlines = scanner.splitlines()[1:]
            pointlist = []
            for sline in scanlines:
                x, y, z = sline.split(",")
                pointlist.append(Point3D(int(x), int(y), int(z)))

            self.scanners.append(Scanner(pointlist))

        self.canon_scanners = [self.scanners[0]]

    def solve_part1(self) -> int:
        """
        Solves part 1, exhaustively. (Hopefully)
        """

        # Queue of all the unsolved scanners
        unsolved = deque(self.scanners[1:])
        while unsolved:
            candidate = unsolved.popleft()

            # Okay, this is a bit complicated.
            # We want to check over every possible rotation and every
            # currently discovered canonical set, and see if the set of
            # scanners matches up. Complicated, and hard to even explain.
            # Let's implement it.
            for rotation, canon in it.product(range(24), self.canon_scanners):
                rotated_candidate = candidate.rotate(rotation)
                sb, ob, inter = canon.compare_dists(rotated_candidate)
                if len(inter) >= 11:
                    # We've got a match!
                    rotated_candidate.translate(sb - ob)
                    self.canon_scanners.append(rotated_candidate)
                    break

            else:
                # We'll come back to it later.
                unsolved.append(candidate)

        # In theory, this should give us the answer.
        all_beacons = set()
        for scanner in self.canon_scanners:
            for beacon in scanner.beacons:
                all_beacons.add(beacon)

        return len(all_beacons)

    def solve_part2(self) -> int:
        """
        Finds the largest Manhattan distance between any two scanners.
        """

        max_dist = 0
        for s1 in self.canon_scanners:
            for s2 in self.canon_scanners:
                if s1 is s2:
                    continue

                diff = s1.location - s2.location
                max_dist = max(max_dist, diff.l1_norm())

        return max_dist


if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument(
        "-e",
        "--example",
        help="Use the example file for input instead of main",
        action="store_true",
    )

    args = parser.parse_args()
    day = re.search(r"\d+", sys.argv[0]).group(0)
    filename = f"inputs/d{day}.txt"
    if args.example:
        filename = f"inputs/d{day}ex.txt"

    sol = Solution(filename)
    print(f"Part 1: {sol.solve_part1()}")
    print(f"Part 2: {sol.solve_part2()}")
