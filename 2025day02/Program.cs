using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

class Solver
{
    public long FirstHalf;
    public int Repetitions;

    public Solver(string composite, int repetitions) {
        long compositeAsInt = Int64.Parse(composite);
        Repetitions = repetitions;
        if (composite.Length < Repetitions) {
            FirstHalf = 1;
        } else {
            FirstHalf = Int64.Parse(composite[0..(composite.Length / Repetitions)]); // round down
        }
        while (CurrentNumber() < compositeAsInt) {
            Increment();
        }
    }

    public long CurrentNumber() {
        var sb = new StringBuilder();
        var partAsString = FirstHalf.ToString();
        for (int i = 0; i < Repetitions; ++i) {
            sb.Append(partAsString);
        }
        return Int64.Parse(sb.ToString());
    }

    public void Increment() {
        FirstHalf += 1;
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
            var invalidIds = new HashSet<long>();
            foreach (string interval in line.Split(',')) {
                Console.WriteLine(interval);
                string[] parts = interval.Split('-');
                var end = Int64.Parse(parts[1]);
                for (int repetitions = 2; repetitions < 20; ++repetitions) {
                    for (var enumerator = new Solver(parts[0], repetitions); enumerator.CurrentNumber() <= end; enumerator.Increment()) {
                        Console.WriteLine(" -> " + enumerator.CurrentNumber());
                        invalidIds.Add(enumerator.CurrentNumber());
                    }
                }
            }
            long sumOfInvalidIds = 0;
            foreach (long invalidId in invalidIds) {
                sumOfInvalidIds += invalidId;
            }
            Console.WriteLine("sum = " + sumOfInvalidIds);
        }
    }
}
