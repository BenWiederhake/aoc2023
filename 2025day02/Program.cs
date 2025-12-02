using System.Collections.Generic;
using System;
using System.Diagnostics;

class Solver
{
    public long firstHalf;

    public Solver(string composite) {
        long compositeAsInt = Int64.Parse(composite);
        if (composite.Length < 2) {
            firstHalf = 1;
        } else {
            firstHalf = Int64.Parse(composite[0..(composite.Length / 2)]); // round down
        }
        while (CurrentNumber() < compositeAsInt) {
            Increment();
        }
    }

    public long CurrentNumber() {
        return Int64.Parse("" + firstHalf + firstHalf);
    }

    public void Increment() {
        firstHalf += 1;
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        using (StreamReader sr = new StreamReader(filename))
        {
            Debug.Assert(sr != null);
            string line = sr.ReadLine();
            Debug.Assert(line != null);
            long sumOfInvalidIds = 0;
            foreach (string interval in line.Split(',')) {
                Console.WriteLine(interval);
                string[] parts = interval.Split('-');
                var end = Int64.Parse(parts[1]);
                for (var enumerator = new Solver(parts[0]); enumerator.CurrentNumber() <= end; enumerator.Increment()) {
                    Console.WriteLine(" -> " + enumerator.CurrentNumber());
                    sumOfInvalidIds += enumerator.CurrentNumber();
                }
            }
            Console.WriteLine(sumOfInvalidIds);
        }
    }
}
