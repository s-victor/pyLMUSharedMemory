"""
LMU Memory Map Control

Inherit Python mapping of LMU Shared Memory Interface
"""

from __future__ import annotations

import ctypes
import logging
import mmap
import platform

try:
    from . import lmu_data
    from .lmu_data import LMUConstants
except ImportError:  # standalone, not package
    import lmu_data
    from lmu_data import LMUConstants

PLATFORM = platform.system()
MAX_VEHICLES = LMUConstants.MAX_MAPPED_VEHICLES
INVALID_INDEX = -1


def get_root_logger_name():
    """Get root logger name"""
    for logger_name in logging.root.manager.loggerDict:
        return logger_name
    return __name__


logger = logging.getLogger(get_root_logger_name())


class MMapControl:
    """Memory map control"""

    __slots__ = (
        "_mmap_name",
        "_mmap_buffer",
        "_struct",
        "_buffer",
        "_realtime",
        "update",
        "data",
    )

    def __init__(self, mmap_name: str, data_struct: ctypes.Structure) -> None:
        """Initialize memory map setting

        Args:
            mmap_name: mmap filename.
            data_struct: ctypes data structure, ex. lmu_data.SharedMemoryEvent.
        """
        self._mmap_name = mmap_name
        self._mmap_buffer = None
        self._struct = data_struct
        self._buffer = bytearray()
        self._realtime = None
        self.update = None
        self.data = None

    def __del__(self):
        logger.info("sharedmemory: GC: MMap %s", self._mmap_name)

    def create(self, access_mode: int = 0) -> None:
        """Create mmap instance & initial accessible copy

        Args:
            access_mode: 0 = copy access, 1 = direct access.
        """
        self._mmap_buffer = mmap.mmap(-1, ctypes.sizeof(self._struct), self._mmap_name)

        if access_mode:
            self.data = self._struct.from_buffer(self._mmap_buffer)
            self.update = self.__buffer_share
        else:
            self._buffer[:] = self._mmap_buffer
            self._realtime = self._struct.from_buffer(self._mmap_buffer)
            self.data = self._struct.from_buffer(self._buffer)
            self.update = self.__buffer_copy

        mode = "Direct" if access_mode else "Copy"
        logger.info("sharedmemory: ACTIVE: %s (%s Access)", self._mmap_name, mode)

    def close(self) -> None:
        """Close memory mapping

        Create a final accessible mmap data copy before closing mmap instance.
        """
        self.data = self._struct.from_buffer_copy(self._mmap_buffer)
        self._realtime = None
        try:
            self._mmap_buffer.close()
            logger.info("sharedmemory: CLOSED: %s", self._mmap_name)
        except BufferError:
            logger.error("sharedmemory: buffer error while closing %s", self._mmap_name)
        self.update = None  # unassign update method (for proper garbage collection)

    def __buffer_share(self) -> None:
        """Share buffer access, may result data desync"""

    def __buffer_copy(self) -> None:
        """Copy buffer access, helps avoid data desync"""
        # Check if game updating data
        if (
            self._realtime.generic.events.SME_UPDATE_SCORING
            or self._realtime.generic.events.SME_UPDATE_TELEMETRY
        ) and (
            self._realtime.scoring.scoringInfo.mNumVehicles
            == self._realtime.telemetry.activeVehicles
        ):
            self._buffer[:] = self._mmap_buffer


def test_api():
    """API test run"""
    # Add logger
    test_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.addHandler(test_handler)

    # Test run
    SEPARATOR = "=" * 50
    print("Test API - Direct Access")
    info = MMapControl(LMUConstants.LMU_SHARED_MEMORY_FILE, lmu_data.LMUObjectOut)
    info.create(1)
    info.update()

    print(SEPARATOR)
    print("Test API - Close")
    info.close()

    print(SEPARATOR)
    print("Test API - Copy Access")
    info.create(0)
    info.update()

    print(SEPARATOR)
    print("Test API - Read")
    version = info.data.generic.gameVersion
    track = info.data.scoring.scoringInfo.mTrackName.decode()
    vehicle = info.data.telemetry.telemInfo[0].mVehicleName.decode()
    total = info.data.scoring.scoringInfo.mNumVehicles
    print(f"version: {version if version else 'not running'}")
    print(f"track name: {track if version else 'not running'}")
    print(f"vehicle name: {vehicle if version else 'not running'}")
    print(f"total cars: {total if version else 'not running'}")

    print(SEPARATOR)
    info.close()


if __name__ == "__main__":
    test_api()
