from dataclasses import dataclass
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывести сообщение о тренировке"""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Метод get_spent_calories "
                                  "в классе Training не определен")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return message


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1
                 * self.get_mean_speed()
                 - self.COEFF_CALORIE_2)
                * self.weight_kg
                / self.M_IN_KM
                * self.duration_h
                * self.MIN_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height_sm: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.COEFF_CALORIE_1 * self.weight_kg
                + (self.get_mean_speed()
                   ** 2
                   // self.height_sm)
                * self.COEFF_CALORIE_2
                * self.weight_kg)
                * self.duration_h
                * self.MIN_IN_HOUR
                )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.count_pool
                * self.length_pool
                / self.M_IN_KM
                / self.duration_h
                )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
               (self.get_mean_speed()
                + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight_kg
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    try:
        workout = workout_type_dict[workout_type](*data)
        return workout
    except KeyError:
        raise KeyError("Тип тренировки не опознан")


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
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
