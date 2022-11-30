class SleepController:
    def __init__(self, config):
        self.backoff = self.backoff_start = config.backoff_start
        self.backoff_stop = config.backoff_stop
        self.backoff_multiple = config.backoff_multiple

    def current_backoff(self) -> int:
        current_backoff = self.backoff
        self.backoff *= self.backoff_multiple
        self.backoff = self.backoff_stop if self.backoff > self.backoff_stop else self.backoff
        return current_backoff

    def reset(self) -> None:
        self.backoff = self.backoff_start
