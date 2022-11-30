from sleep_controller import SleepController


def test_sleep_controller(config):
    sleep_controller = SleepController(config)
    assert sleep_controller.current_backoff() < sleep_controller.backoff_start * 2


def test_sleep_reset(config):
    sleep_controller = SleepController(config)
    sleep_controller.current_backoff()
    sleep_controller.current_backoff()
    sleep_controller.current_backoff()
    assert sleep_controller.current_backoff() > sleep_controller.backoff_start * 2
    sleep_controller.reset()
    assert sleep_controller.current_backoff() == config.backoff_start


def test_sleep_controller_reached_max(config):
    sleep_controller = SleepController(config)
    sleep_controller.current_backoff()
    for _ in range(100):
        sleep_controller.current_backoff()

    assert sleep_controller.current_backoff() == config.backoff_stop
