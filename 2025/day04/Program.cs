using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

class Solver
{
    public List<char[]> Map { get; }
    public int W { get; }
    public int H { get; }

    public Solver(List<char[]> map) {
        Map = map;
        Debug.Assert(Map.Count > 0);
        W = Map[0].Length;
        H = Map.Count;
    }

    public bool IsAccessiblePaperRoll(int x, int y) {
        if (Map[y][x] != '@') {
            // There's no paper roll here, therefore there's no *accessible* paper roll here either.
            return false;
        }
        int rollsInTheWayIncludingSelf = 0;
        for (int dy = -1; dy < 1 + 1; ++dy) {
            for (int dx = -1; dx < 1 + 1; ++dx) {
                int nx = x + dx;
                int ny = y + dy;
                if (nx < 0 || nx >= W || ny < 0 || ny >= H) {
                    // Not a valid position, skip it
                    continue;
                }
                if (Map[ny][nx] == '@') {
                    rollsInTheWayIncludingSelf += 1;
                }
            }
        }
        return (rollsInTheWayIncludingSelf - 1) < 4;
    }

    public int CountAndRemoveAccessiblePaperRolls() {
        int numAccessible = 0;
        for (int y = 0; y < H; ++y) {
            for (int x = 0; x < W; ++x) {
                if (IsAccessiblePaperRoll(x, y)) {
                    // It's fine to remove it already! After all, we don't need to determine the "level" of each roll.
                    Map[y][x] = '.';
                    numAccessible += 1;
                }
            }
        }
        return numAccessible;
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        var map = new List<char[]>();
        using (StreamReader sr = new StreamReader(filename))
        {
            Debug.Assert(sr != null);
            string line;
            while ((line = sr.ReadLine()) != null) {
                map.Add(line.ToCharArray());
            }
        }
        var solver = new Solver(map);
        int totalCount = 0;
        int iterations = 0;
        while (true) {
            var removedInThisIteration = solver.CountAndRemoveAccessiblePaperRolls();
            if (removedInThisIteration == 0) {
                break;
            }
            iterations += 1;
            totalCount += removedInThisIteration;
        }
        Console.WriteLine("iter = " + iterations);
        // Thankfully, the inputs are small enough that no further optimizations are necessary.
        // However, there might be causal sequences of "1-1-1-1-1" removals that might drag out the runtime a lot.
        // If that would have happened, my first approach would have been to alternate between going "forwards"
        // and "backwards", in the hope that going backwards cleans up a causal chain in a single pass, thus saving
        // a lot of runtime.
        // Another approach would be to do only a single pass, but then after each removal check each neighbor.
        // This would mean that each position is considered at most 9 times, i.e. O(n^2) runtime, instead of
        // the current O(n^4) worst-case scenario.
        // But again, none of this seems necessary; this solution runs in 120 ms.
        Console.WriteLine("num = " + totalCount);
    }
}
