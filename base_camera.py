import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """Подобный событию класс, который сигнализирует всем активным клиентам, когда доступен новый кадр."""
    def __init__(self):
        self.events = {}

    def wait(self):
        """Вызывается из каждого клиентского потока для ожидания следующего кадра."""
        ident = get_ident()
        if ident not in self.events:
            # это новый клиент
            # добавляем запись для него в self.events dict
            # каждая запись состоит из двух элементов: threading.Event() и timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Вызывается потоком камеры, когда доступен новый кадр."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # если это клиентское событие не установлено, установите его также,
                # чтобы обновить последнюю установленную временную метку до настоящего момента.
                event[0].set()
                event[1] = now
            else:
                # если событие клиента уже установлено, это означает,
                # что клиент не обрабатывал предыдущий кадр,
                # если событие остается установленным более 5 секунд,
                # затем предположите, что клиент ушел, и удалите его
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Вызывается из каждого клиентского потока после обработки кадра."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # фоновый поток, который читает кадры с камеры
    frame = None  # текущий кадр сохраняется здесь фоновым потоком
    last_access = 0  # время последнего обращения клиента к камере
    event = CameraEvent()

    def __init__(self):
        """Запустите поток фоновой камеры, если он еще не запущен."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # начало фоновой рамки потока
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # подождите, пока не станут доступны кадры
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Вернуть текущий кадр камеры."""
        BaseCamera.last_access = time.time()

        # дождитесь сигнала от потока(thread) камеры
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Генератор, возвращающий кадры с камеры."""
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Фотоновая thread камеры."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # посылает сигнал клиентам
            time.sleep(0)

            # если за последние 10 секунд не было ни одного клиента, запрашивающего кадры, остановите поток
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None