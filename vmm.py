#!/usr/bin/env python3

import logging
import sys

from physical_memory import PhysicalMemory
from tlb import TLB


class VirtualMemoryManager:
    """
    Implementa um gerenciador de memória virtual, o qual possui memória física, tabela de páginas e
    TLB.
    """

    OUTPUT_FILE = "output.txt"

    def __init__(
        self,
        tlb_size: int = 16,
        page_table_size: int = 2 ** 8,
        frame_count: int = 2 ** 7,
        frame_size: int = 2 ** 8,
    ) -> None:
        self.tlb = TLB(tlb_size)
        self.page_table: list[int | None] = [None] * page_table_size
        self.physical_memory = PhysicalMemory(frame_count, frame_size)

    @staticmethod
    def get_page_number(address: int) -> int:
        """
        Retorna os 8 primeiros bits de um endereço de 16 bits.
        """
        return address >> 8

    @staticmethod
    def get_offset(address: int) -> int:
        """
        Usa um bitmask para selecionar os 8 últimos bits de um endereço de 16 bits.
        """
        return address & 0x00FF

    def get_physical_address(self, frame_number: int, offset: int):
        """
        Calcula um endereço físico a partir de um número de quadro e offset.
        """
        return frame_number * self.physical_memory.frame_size + offset

    def read_addresses(self, addresses_file_path: str) -> None:
        """
        Lê um arquivo contendo endereços lógicos e transforma cada linha em um endereço físico.
        Também apresenta o número de page faults e TLB hits do programa.
        """
        addresses_count = 0
        page_faults = 0
        tlb_hits = 0

        with open(addresses_file_path, "rb") as file, open(
            self.OUTPUT_FILE, "w", encoding="utf-8"
        ) as output:
            for line in file.readlines():
                virtual_address = int(line)
                page_number = self.get_page_number(virtual_address)
                offset = self.get_offset(virtual_address)
                logging.debug("Número de página: %d, Offset: %d", page_number, offset)

                frame_number = self.tlb.get_frame_number(page_number)
                if frame_number:
                    logging.debug("TLB hit, %d está na TLB", page_number)
                    tlb_hits += 1
                else:
                    # Endereço não está presente na TLB.
                    if page_number in self.physical_memory.lru:
                        logging.debug(
                            "Número de página %d está presente na tabela de páginas",
                            page_number,
                        )
                        frame_number = self.page_table[page_number]
                    else:
                        # Endereço não está presente na tabela de páginas, é preciso adiciona-lo a
                        # memória física primeiro.
                        logging.debug(
                            "Page fault, número de página %d não está na tabela de páginas",
                            page_number,
                        )
                        frame_number = self.physical_memory.read_frame_from_backing_store(
                            page_number, self.page_table
                        )
                        self.page_table[page_number] = frame_number
                        page_faults += 1
                    self.tlb.add(page_number, frame_number)

                # Atualiza a frequência de acesso do número de página atual.
                self.physical_memory.update_lru(page_number)
                physical_address = self.get_physical_address(frame_number, offset)
                logging.debug(
                    "Página %d corresponde ao quadro %d na memória física,"
                    " endereço virtual: %d, endereço físico: %d, conteúdo: %d",
                    page_number,
                    frame_number,
                    virtual_address,
                    physical_address,
                    self.physical_memory[physical_address],
                )

                output_string = (
                    f"Endereço Virtual: {virtual_address}"
                    f" Endereço Físico: {physical_address}"
                    f" Conteúdo: {self.physical_memory[physical_address]}\n"
                )
                print(output_string, end="")
                output.write(output_string)
                addresses_count += 1

            statistics_string = (
                f"Page fault: {round((page_faults / addresses_count) * 100, 2)}%\n"
                f"TLB hit: {round((tlb_hits/ addresses_count) * 100, 2)}%\n"
            )
            print(statistics_string, end="")
            output.write(statistics_string)


def main():
    if len(sys.argv) <= 1:
        print(
            "ERRO: Forneça o arquivo contendo os endereços lógicos para o programa!",
            file=sys.stderr,
        )
        sys.exit(1)
    # Habilita mensagens de debug
    # logging.basicConfig(level=logging.DEBUG)

    file_path = sys.argv[1]
    vmm = VirtualMemoryManager()
    vmm.read_addresses(file_path)


if __name__ == "__main__":
    main()
