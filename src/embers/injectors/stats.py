class stats:
    start_time = 0
    end_time = 0
    nb_devices = 0
    nb_sent = 0
    time_overflow = []

    def dump(self): dump_stats(self)


def dump_stats(stats):
    nb_sent = stats.nb_sent
    duration = stats.end_time - stats.start_time if stats.end_time else 0
    print("total: {} event{s} sent in {:.1f} sec.".format(
          nb_sent, duration, s="s" if nb_sent != 1 else ""))

    if not stats.time_overflow: return

    def avg(x): return sum(x)/len(x)
    print("==> time overflow: {avg:.2f} sec.  {note}".format(
          avg=avg(stats.time_overflow),
          note="nb-devices x ev-per-hour too high",
    ))
