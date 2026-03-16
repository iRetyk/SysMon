

questions:

While writing collector.get_memory, i've noticed the the used + available is drasticly different from the total amount of memory. (~ 5gb compared to ~8gb)
With a little research ive seen that the gap consists mainly of OS reserved memory,  buffers and caches.
I am not satisfied with this answer (the gap is too big), and more research is due.  
after researching specify about mac (which am i using) it is very common that apps like chrome have several GB of compressed data which isn't accounted for in the used/available fields.


sources:

https://docs.python.org/3/howto/argparse.html - argparse doc