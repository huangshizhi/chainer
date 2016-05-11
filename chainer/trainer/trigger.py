class IntervalTrigger(object):

    """Trigger based on a fixed interval.

    This trigger accepts iterations divided by a given interval. There are two
    ways to specify the interval: per iterations and epochs. `Iteration` means
    the number of updates, while `epoch` means the number of sweeps over the
    training dataset. Both values are defined by the updater.

    For the description of triggers, see :func:`get_trigger`.

    Args:
        period (int): Length of the interval.
        unit (str): Unit of the length specified by ``period``. It must be
            either ``'iteration'`` or ``'epoch'``.

    """
    def __init__(self, period, unit):
        self.period = period
        assert unit == 'epoch' or unit == 'iteration'
        self.unit = unit

    def __call__(self, trainer):
        """Decides whether the extension should be called on this iteration.

        Args:
            trainer (Trainer): Trainer object that currently runs.

        Returns:
            bool: True if the corresponding extension should be invoked in this
                iteration.

        """
        updater = trainer.updater
        if self.unit == 'epoch':
            return updater.is_new_epoch and updater.epoch % self.period == 0
        else:
            return updater.iteration % self.period == 0


def get_trigger(trigger):
    """Gets a trigger object.

    If ``trigger`` is callable, it just returns the trigger. Otherwise, it
    passes the value to :class:`IntervalTrigger`.

    """
    if callable(trigger):
        return trigger
    else:
        return IntervalTrigger(*trigger)
