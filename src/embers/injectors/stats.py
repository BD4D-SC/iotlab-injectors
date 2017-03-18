class stats:
    start_time = 0
    end_time = 0
    nb_devices = 0
    nb_loops = 0
    time_overflow = []

    def dump(self): dump_stats(self)


def dump_stats(stats):
    nb_sent = stats.nb_loops * stats.nb_devices
    duration = stats.end_time - stats.start_time
    print("total: {} event{s} sent in {:.1f} sec.".format(
          nb_sent, duration, s="s" if nb_sent != 1 else ""))

    if not stats.time_overflow: return

    def avg(x): return sum(x)/len(x)
    print("==> time overflow: {avg:.2f} sec.  {note}".format(
          avg=avg(stats.time_overflow),
          note="nb-devices x ev-per-hour too high",
    ))
