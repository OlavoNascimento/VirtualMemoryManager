import logging
from collections import deque
from struct import unpack


class PhysicalMemory:
    """
    Implementa um memória física que utiliza pode ler frames do arquivo BACKING_STORE.
    Quando não há mais espaço na memória o frame menos utilizado é substituído pelo o novo frame.
    """

    BACKING_STORE_PATH = "teste.dat"

    def __init__(self, frame_count: int, frame_size: int) -> None:
        self.capacity = frame_count
        self.frames_in_memory = 0
        self.frame_size = frame_size
        self.physical_memory: list[int | None] = [None] * frame_count * frame_size
        self.lru: deque[int] = deque()

    def update_lru(self, page_number: int) -> int:
        """
        Atualiza a frequência de acesso de um número de página na memória física.
        """
        try:
            self.lru.remove(page_number)
        except ValueError:
            pass
        self.lru.appendleft(page_number)

    def read_frame_from_backing_store(self, page_number: int, page_table: list[int]) -> int:
        """
        Lê um quadro armazenado no backing storage e salva na memória física.
        Utiliza a estratégia LRU para substituir frames.
        """
        if self.frames_in_memory >= self.capacity:
            # Memória está cheia, substitui o frame menos utilizado pelo o frame novo.
            least_used_page_number = self.lru.pop()
            position = page_table[least_used_page_number]
        else:
            position = self.frames_in_memory
            self.frames_in_memory += 1

        logging.debug(
            "Lendo frame %d do backing store, salvando no frame %d da memória física",
            page_number,
            position,
        )

        frame_start = position * self.frame_size
        frame_end = frame_start + self.frame_size
        with open(self.BACKING_STORE_PATH, "rb") as file:
            file.seek(page_number * self.frame_size)

            for i in range(frame_start, frame_end):
                char = file.read(1)
                if not char:
                    break
                (content,) = unpack("B", char)
                logging.debug("Salvando valor %d na posição %d da memória física", content, i)
                self.physical_memory[i] = content

        return position

    def __getitem__(self, key: int) -> int | None:
        return self.physical_memory[key]
