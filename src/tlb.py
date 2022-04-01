import logging
from collections import deque

TLBEntry = (int | None, int | None)


class TLB:
    """
    Implementa uma TLB que utiliza a estratégia LRU para substituir frames.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.tlb: list[TLBEntry] = [(None, None)] * capacity
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

    def add(self, page_number: int, frame_number: int):
        """
        Adiciona um elemento a TLB. Se a TLB estiver cheia o frame menos utilizado é substituído
        pelo novo frame.
        """
        if self.size >= self.capacity:
            position = self.lru.pop()
        else:
            position = self.size
            self.size += 1

        logging.debug(
            "Adicionando page number: %d, frame: %d na TLB (posição: %d)",
            page_number,
            frame_number,
            position,
        )
        self.update_lru(position)
        self.tlb[position] = (page_number, frame_number)

    def get_frame_number(self, page_number: int) -> int | None:
        """
        Retorna o frame de correspondente a uma página, caso não exista retorna None.
        """
        for index, (tlb_page_number, tlb_frame_number) in enumerate(self.tlb):
            if tlb_page_number == page_number:
                self.update_lru(index)
                return tlb_frame_number
        return None
