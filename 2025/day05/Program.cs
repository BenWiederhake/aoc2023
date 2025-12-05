using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

// `Range` instances are immutable.
struct Range : IComparable<Range> {
    public long Lo { get; }
    public long Hi { get; }

    public Range(long lo, long hi) {
        Debug.Assert(lo <= hi);
        Lo = lo;
        Hi = hi;
    }

    public int CompareTo(Range that)
    {
        if (this.Lo <  that.Lo) return -1;
        if (this.Lo == that.Lo) return 0;
        return 1;
    }
}

// `RangeSet` instances are immutable.
class RangeSet {
    private List<Range> SortedRanges;

    public RangeSet(List<Range> sortedRanges) {
        // Console.WriteLine("Got " + sortedRanges.Count + " sorted (and merged) ranges:");
        // foreach (var e in sortedRanges) {
        //     Console.WriteLine(" * " + e.Lo + "-" + e.Hi);
        // }
        SortedRanges = sortedRanges;
    }

    // - Either returns a valid index of a range whose "Lo" is less-or-equal the requested ingredientId (and is the maximum such index),
    // - or returns -1.
    public int IndexOfFloorRange(long ingredientId) {
        // https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.binarysearch?view=net-10.0
        // """
        //     The zero-based index of item in the sorted List<T>, if item is found; otherwise, a negative number
        //     that is the bitwise complement of the index of the next element that is larger than item or,
        //     if there is no larger element, the bitwise complement of Count.
        // """
        // I mean, yes, okay, it *does* conver all cases, but was there really no better way to represent this information?
        // No enum or option type? Really? Oof.
        int binarySearchIndex = SortedRanges.BinarySearch(new Range(ingredientId, ingredientId));
        if (binarySearchIndex >= 0) {
            // Exact match found! "Floor" is just identity function in this case:
            return binarySearchIndex;
        }
        // No exact match found! First, determine a "normal" (i.e. non-negative) index:
        int ceilingIndex = ~binarySearchIndex;
        // `ceilingIndex` might point to the range *after* the last range.
        // Just to make sure I understood this conversion and bitfiddling correctly:
        Debug.Assert(0 <= ceilingIndex && ceilingIndex <= SortedRanges.Count);
        return ceilingIndex - 1;
    }

    public bool Contains(long ingredientId) {
        int onlyRelevantIndex = IndexOfFloorRange(ingredientId);
        // Console.WriteLine($"Looking up {ingredientId}, will look only at index {onlyRelevantIndex}");
        if (onlyRelevantIndex < 0) {
            return false;
        }
        Range r = SortedRanges[onlyRelevantIndex];
        // Console.WriteLine($"  ... which is {r.Lo}-{r.Hi}");
        // if (onlyRelevantIndex + 1 < SortedRanges.Count) {
        //     var next = SortedRanges[onlyRelevantIndex + 1];
        //     Console.WriteLine($"  ... followed by {next.Lo}-{next.Hi}");
        // }
        // Just to sanity check: This is the last range whose `Lo` is less-or-equal the requested ingredientId, right?
        Debug.Assert(r.Lo <= ingredientId);
        Debug.Assert(onlyRelevantIndex + 1 == SortedRanges.Count || ingredientId < SortedRanges[onlyRelevantIndex + 1].Lo);
        return ingredientId <= r.Hi;
    }

    public long SizeOfFreshRanges() {
        long size = 0;
        foreach (var r in SortedRanges) {
            size += r.Hi - r.Lo + 1;
        }
        return size;
    }
}

// `Solver` instances are mutable, similar to `StringBuilder`.
class Solver
{
    private List<Range> UnsortedRanges = new();

    public Solver() {
    }

    public void AddFreshRange(string lo, string hi) {
        Range r = new(Int64.Parse(lo), Int64.Parse(hi));
        // Console.WriteLine($"Parsed {lo}-{hi} as {r.Lo}-{r.Hi}");
        UnsortedRanges.Add(r);
    }

    public RangeSet ToRangeSet() {
        // Console.WriteLine("Got " + UnsortedRanges.Count + " raw (unsorted, unmerged) ranges:");
        // foreach (var e in UnsortedRanges) {
        //     Console.WriteLine(" * " + e.Lo + "-" + e.Hi);
        // }
        UnsortedRanges.Sort();
        List<Range> sortedRanges = new();
        Range? pending = null;
        foreach (var range in UnsortedRanges) {
            if (pending.HasValue && pending.Value.Hi + 1 < range.Lo) {
                // Flush:
                sortedRanges.Add(pending.Value);
                pending = null;
                // Fall-through to "Take"
            }
            if (!pending.HasValue) {
                // Take:
                pending = range;
            } else {
                // Merge:
                pending = new Range(pending.Value.Lo, Math.Max(pending.Value.Hi, range.Hi));
            }
        }
        if (pending.HasValue) {
            // Flush:
            sortedRanges.Add(pending.Value);
            pending = null;
        }
        return new RangeSet(sortedRanges);
    }

    static void Main(string[] args)
    {
        string filename = "input";
        if (args.Length > 0) {
            filename = args[0];
        }
        int numFreshIngredients = 0;
        using (StreamReader sr = new StreamReader(filename))
        {
            string line;
            Solver solver = new();
            while ((line = sr.ReadLine()) != null && (line != "")) {
                var parts = line.Split('-');
                solver.AddFreshRange(parts[0], parts[1]);
            }
            var rangeSet = solver.ToRangeSet();
            Console.WriteLine("size of fresh ranges = " + rangeSet.SizeOfFreshRanges());
            //while ((line = sr.ReadLine()) != null) {
            //    if (rangeSet.Contains(Int64.Parse(line))) {
            //        numFreshIngredients += 1;
            //    }
            //}
        }
        //Console.WriteLine("numFresh = " + numFreshIngredients);
    }
}
