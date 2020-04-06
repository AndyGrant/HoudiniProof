The following code appears in Houdini 6's ``zoek_smp.cpp``. Translating to English, this loop goes through each of the active threads and sums up the total nodes searched. Before returning that value, however, the value is increased by ``knopen / 7``.

```
uint64_t ThreadPool::bezochte_knopen()
{
	uint64_t knopen = 0;
	for (int i = 0; i < activeThreadCount; ++i)
		knopen += threads[i]->rootStelling->bezochte_knopen();
	knopen += knopen / 7;
	return knopen;
}
```

Due to how integer arithmetic works on a CPU, given any ``N``, it can be shown that if you let ``X = N + N/7``, then ``X % 8 != 7``. This repository proves that the version of Houdini that has participated in the Division Premier of TCEC seasons 13, 14, 15, and 16, contains the above code.

The file ``parse.py`` reads the PGN files from each DivP of TCEC seasons 13, 14, 15, and 16, and collects the node counts that Houdini outputs. That data is found in ``output.txt`` and I encourage you to reproduce my results. If we then take all the node values ``N``, and generate a histogram of ``N % 8``, the following is the result:

``0: 1746, 1: 1741, 2: 1725, 3: 1704, 4: 1652, 5: 1687, 6: 1733, 7: 0``

This histogram provides damning proof that Houdini's output for nodes searched is modified like the code above. The code above appears in Houdini 6's source files.

I believe that Houdini is a direct clone of Stockfish, and is in violation of the GPL.
