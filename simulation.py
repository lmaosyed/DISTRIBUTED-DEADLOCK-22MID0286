import simpy
import random

class Site:
    def __init__(self, site_id):
        self.site_id = site_id
        self.wfg = {}

    def add_edge(self, p1, p2):
        if p1 not in self.wfg:
            self.wfg[p1] = []
        self.wfg[p1].append(p2)

    def get_waiting(self, process):
        return self.wfg.get(process, [])


class DistributedSystem:
    def __init__(self, env, num_sites):
        self.env = env
        self.sites = [Site(i) for i in range(num_sites)]
        self.logs = []
        self.edges = []
        self.deadlocks = set()

    def log(self, message):
        self.logs.append(message)

    def send_probe(self, initiator, sender, receiver):
        yield self.env.timeout(1)

        self.log(f"Probe: ({initiator}, {sender} → {receiver})")

        # DEADLOCK CONDITION
        if receiver == initiator:
            self.log(f"🚨 DEADLOCK DETECTED involving {initiator}")
            self.deadlocks.add(initiator)
            return

        # propagate probe
        for site in self.sites:
            if receiver in site.wfg:
                for next_p in site.get_waiting(receiver):
                    self.env.process(
                        self.send_probe(initiator, receiver, next_p)
                    )


def process_behavior(env, system, site, process_id):
    while True:
        yield env.timeout(random.randint(1, 3))

        target = f"P{random.randint(1, 5)}"

        if target != process_id:
            site.add_edge(process_id, target)

            system.edges.append((process_id, target))
            system.log(f"{process_id} waits for {target}")

            env.process(system.send_probe(process_id, process_id, target))


def run_simulation_with_graph():
    env = simpy.Environment()
    system = DistributedSystem(env, num_sites=2)

    for i in range(1, 6):
        site = random.choice(system.sites)
        env.process(process_behavior(env, system, site, f"P{i}"))

    env.run(until=15)

    return system.logs, system.edges, list(system.deadlocks)