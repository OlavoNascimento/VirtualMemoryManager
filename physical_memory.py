import logging
from collections import deque
from struct import unpack


class PhysicalMemory:
    BACKING_STORE_PATH = "teste.dat"

    def __init__(self, frame_count: int, frame_size: int) -> None:
        self.max_frame_count = frame_count
        self.frame_size = frame_size
        self.frames_in_memory = 0
        self.physical_memory: list[int | None] = [None] * frame_count * frame_size
        self.lru: deque[int] = deque()

    def update_lru(self, position: int) -> int:
        """
        Atualiza a frequência de acesso de um frame na memória física.
        """
        try:
            self.lru.remove(position)
        except ValueError:
            pass
        self.lru.appendleft(position)

    def read_frame_from_backing_store(self, page_number: int) -> int:
        """
        Lê um frame armazenado no backing storage e salva na memória física.
        """
        if self.frames_in_memory >= self.max_frame_count:
            position = self.lru.pop()
        else:
            position = self.frames_in_memory
            self.frames_in_memory += 1

        logging.debug(
            "Lendo frame %d do backing store, salvando no frame %d da memória física",
            page_number,
            position,
        )
        self.update_lru(position)

        frame_start = position * self.frame_size
        with open(self.BACKING_STORE_PATH, "rb") as file:
            file.seek(page_number * self.frame_size)
            for i in range(self.frame_size):
                char = file.read(1)
                if not char:
                    break
                (content,) = unpack("B", char)
                logging.debug(
                    "Salvando valor %d na posição %d da memória física", content, frame_start + i
                )
                self.physical_memory[frame_start + i] = content

        return position

    def __getitem__(self, key: int) -> int | None:
        return self.physical_memory[key]
