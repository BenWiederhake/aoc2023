using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

class Solver
{
    static int FindJoltage(char[] bank) {
        char firstChar = bank[..(bank.Length - 1)].Max();
        int firstCharIndex = Array.IndexOf(bank, firstChar);
        char secondChar = bank[(firstCharIndex + 1)..].Max();
        int result = Int32.Parse("" + firstChar + secondChar);
        Console.WriteLine("+ " + result);
        return result;
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        int sumOfJoltages = 0;
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
