using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

class Solver
{
    const int JOLTAGE_DIGITS = 12;

    static long FindJoltage(char[] bank) {
        Debug.Assert(bank.Length >= JOLTAGE_DIGITS);
        int firstValidIndex = 0;
        var sb = new StringBuilder();
        for (int i = 0; i < JOLTAGE_DIGITS; ++i) {
            char taken = bank[firstValidIndex..(bank.Length - JOLTAGE_DIGITS + i + 1)].Max();
            sb.Append(taken);
            firstValidIndex = Array.IndexOf(bank, taken, firstValidIndex) + 1;
        }
        long result = Int64.Parse(sb.ToString());
        Console.WriteLine("+ " + result);
        return result;
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        long sumOfJoltages = 0;
        using (StreamReader sr = new StreamReader(filename))
        {
            Debug.Assert(sr != null);
            string line;
            while ((line = sr.ReadLine()) != null) {
                sumOfJoltages += FindJoltage(line.ToCharArray());
            }
        }
        Console.WriteLine("sum = " + sumOfJoltages);
    }
}
