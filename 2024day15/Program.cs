using System.Collections.Generic;
using System;
using System.Diagnostics;

class Solver
{
    public List<char[]> CurrentMap;
    public int W { get; }
    public int H { get; }
    public int RobotX, RobotY;

    public Solver(List<char[]> map) {
        CurrentMap = map;
        W = map[0].Length;
        H = map.Count;
        var isFound = false;
        for (int y = 0; y < H && !isFound; ++y) {
            for (int x = 0; x < W; ++x) {
                if (CurrentMap[y][x] == '@') {
                    RobotX = x;
                    RobotY = y;
                    CurrentMap[y][x] = '.';
                    isFound = true;
                }
            }
        }
        Debug.Assert(isFound);
    }

    public void Step(char direction) {
        int dx = 0;
        int dy = 0;
        switch (direction) {
            case '>': dx = 1; break;
            case '<': dx = -1; break;
            case 'v': dy = 1; break;
            case '^': dy = -1; break;
            default: Debug.Assert(false); break;
        }
        var nextPosX = RobotX + dx;
        var nextPosY = RobotY + dy;
        // Find the first "next" position that is not a crate:
        for (; CurrentMap[nextPosY][nextPosX] == 'O'; nextPosX += dx, nextPosY += dy);
        switch (CurrentMap[nextPosY][nextPosX]) {
            case '#':
                // Obstacle or wall. Don't move the robot, don't move any crates.
                return;
            case '.':
                // Free space! Great, let's move the box there, if any.
                CurrentMap[nextPosY][nextPosX] = 'O';
                RobotX += dx;
                RobotY += dy;
                // This overwrites the previous crate-write if there are zero crates:
                CurrentMap[RobotY][RobotX] = '.';
                // In all other cases, this technically adds a new crate and destroys an old crate, instead of moving them.
                // However, since all crates are identical, there is no observable difference.
                return;
            default:
                // '@': Initial robot position. Shouldn't be present anymore.
                // 'O': Crate. Should have been skipped.
                // (out of bounds): Impossible, wall should have been there.
                // (other character): Unspecified behavior. Let's just crash.
                Console.WriteLine(CurrentMap[nextPosY][nextPosX]);
                Debug.Assert(false);
                break;
        }
    }

    public int ComputeGpsCoordSum() {
        int accumulated_sum = 0;
        for (int y = 0; y < H; ++y) {
            for (int x = 0; x < W; ++x) {
                if (CurrentMap[y][x] == 'O') {
                    accumulated_sum += 100 * y + x;
                }
            }
        }
        return accumulated_sum;
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        var map = new List<char[]>();
        var movements = new List<char>();
        using (StreamReader sr = new StreamReader(filename))
        {
            Debug.Assert(sr != null);
            string line;
            while (true)
            {
                line = sr.ReadLine();
                Debug.Assert(line != null);
                if (line.Length == 0) {
                    break;
                }
                map.Add(line.ToCharArray());
            }
            while ((line = sr.ReadLine()) != null)
            {
                movements.AddRange(line.ToCharArray());
            }
        }

        var solver = new Solver(map);
        foreach (char direction in movements) {
            solver.Step(direction);
        }
        for (int y = 0; y < solver.H; ++y) {
            for (int x = 0; x < solver.W; ++x) {
                Console.Write(solver.CurrentMap[y][x]);
            }
            Console.WriteLine();
        }
        var gpsCoordSum = solver.ComputeGpsCoordSum();
        Console.WriteLine(gpsCoordSum);
    }
}
