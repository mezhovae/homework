class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action_times = action
        self.duration_hour = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action_times * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__,
                            self.duration_hour,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight_kg / self.M_IN_KM * (
                self.duration_hour * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.029
    CALORIES_MEAN_SPEED_SHIFT: float = 0.035
    VVOZVIDENIE: int = 2
    KM_M: float = 0.278
    K100: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height_cm = height / self.K100

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время ходьбы."""
        SPEED_IN_M = self.KM_M * self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_SHIFT * self.weight_kg
                + (SPEED_IN_M ** self.VVOZVIDENIE / self.height_cm)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight_kg)
                * (self.duration_hour * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    MNOZITEL: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_meters = length_pool
        self.count_pool_times = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения во время плавания."""

        return (self.length_pool_meters * self.count_pool_times
                / self.M_IN_KM / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время плавания."""

        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.MNOZITEL * self.weight_kg * self.duration_hour)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data: dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_data:
        raise ValueError('Передан неверный идентификатор тренировки.')
    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
