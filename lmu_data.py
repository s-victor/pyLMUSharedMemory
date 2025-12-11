"""
Python mapping of LMU's built-in Shared Memory Interface

This library is based on:
- LMU SharedMemoryInterface header file by S397, found in game's `Support\\SharedMemoryInterface` folder.
- pyRfactor2SharedMemory by Tony Whitley: https://github.com/TonyWhitley/pyRfactor2SharedMemory
"""

import ctypes
import mmap


class LMUConstants:
    LMU_SHARED_MEMORY_FILE: str = "LMU_Data"
    LMU_PROCESS_NAME: str = "Le Mans Ultimate"

    MAX_MAPPED_VEHICLES: int = 104
    MAX_PATH_LENGTH: int = 260  # maximum length for path on windows


# InternalsPlugin

class LMUVect3(ctypes.Structure):
    """Mapping of 'TelemVect3' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double),
    ]


class LMUWheel(ctypes.Structure):
    """Mapping of 'TelemWheelV01' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mSuspensionDeflection", ctypes.c_double),         # meters
        ("mRideHeight", ctypes.c_double),                   # meters
        ("mSuspForce", ctypes.c_double),                    # pushrod load in Newtons
        ("mBrakeTemp", ctypes.c_double),                    # Celsius
        ("mBrakePressure", ctypes.c_double),                # currently 0.0-1.0, depending on driver input and brake balance; will convert to true brake pressure (kPa) in future
        ("mRotation", ctypes.c_double),                     # radians/sec
        ("mLateralPatchVel", ctypes.c_double),              # lateral velocity at contact patch
        ("mLongitudinalPatchVel", ctypes.c_double),         # longitudinal velocity at contact patch
        ("mLateralGroundVel", ctypes.c_double),             # lateral velocity at contact patch
        ("mLongitudinalGroundVel", ctypes.c_double),        # longitudinal velocity at contact patch
        ("mCamber", ctypes.c_double),                       # radians (positive is left for left-side wheels, right for right-side wheels)
        ("mLateralForce", ctypes.c_double),                 # Newtons
        ("mLongitudinalForce", ctypes.c_double),            # Newtons
        ("mTireLoad", ctypes.c_double),                     # Newtons
        ("mGripFract", ctypes.c_double),                    # an approximation of what fraction of the contact patch is sliding
        ("mPressure", ctypes.c_double),                     # kPa (tire pressure)
        ("mTemperature", ctypes.c_double*3),                # Kelvin (subtract 273.15 to get Celsius), left/center/right (not to be confused with inside/center/outside!)
        ("mWear", ctypes.c_double),                         # wear (0.0-1.0, fraction of maximum) ... this is not necessarily proportional with grip loss
        ("mTerrainName", ctypes.c_char*16),                 # the material prefixes from the TDF file
        ("mSurfaceType", ctypes.c_ubyte),                   # 0=dry, 1=wet, 2=grass, 3=dirt, 4=gravel, 5=rumblestrip, 6 = special
        ("mFlat", ctypes.c_bool),                           # whether tire is flat
        ("mDetached", ctypes.c_bool),                       # whether wheel is detached
        ("mStaticUndeflectedRadius", ctypes.c_ubyte),       # tire radius in centimeters
        ("mVerticalTireDeflection", ctypes.c_double),       # how much is tire deflected from its (speed-sensitive) radius
        ("mWheelYLocation", ctypes.c_double),               # wheel's y location relative to vehicle y location
        ("mToe", ctypes.c_double),                          # current toe angle w.r.t. the vehicle
        ("mTireCarcassTemperature", ctypes.c_double),       # rough average of temperature samples from carcass (Kelvin)
        ("mTireInnerLayerTemperature", ctypes.c_double*3),  # rough average of temperature samples from innermost layer of rubber (before carcass) (Kelvin)
        ("mExpansion", ctypes.c_ubyte*24),                  # for future use
    ]


class LMUVehicleTelemetry(ctypes.Structure):
    """Mapping of 'TelemInfoV01' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),                                # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ("mDeltaTime", ctypes.c_double),                      # time since last update (seconds)
        ("mElapsedTime", ctypes.c_double),                    # game session time
        ("mLapNumber", ctypes.c_int),                         # current lap number
        ("mLapStartET", ctypes.c_double),                     # time this lap was started
        ("mVehicleName", ctypes.c_char*64),                   # current vehicle name
        ("mTrackName", ctypes.c_char*64),                     # current track name
        ("mPos", LMUVect3),                                   # world position in meters
        ("mLocalVel", LMUVect3),                              # velocity (meters/sec) in local vehicle coordinates
        ("mLocalAccel", LMUVect3),                            # acceleration (meters/sec^2) in local vehicle coordinates
        ("mOri", LMUVect3*3),                                 # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
        ("mLocalRot", LMUVect3),                              # rotation (radians/sec) in local vehicle coordinates
        ("mLocalRotAccel", LMUVect3),                         # rotational acceleration (radians/sec^2) in local vehicle coordinates
        ("mGear", ctypes.c_int),                              # -1=reverse, 0=neutral, 1+ = forward gears
        ("mEngineRPM", ctypes.c_double),                      # engine RPM
        ("mEngineWaterTemp", ctypes.c_double),                # Celsius
        ("mEngineOilTemp", ctypes.c_double),                  # Celsius
        ("mClutchRPM", ctypes.c_double),                      # clutch RPM
        ("mUnfilteredThrottle", ctypes.c_double),             # ranges  0.0-1.0
        ("mUnfilteredBrake", ctypes.c_double),                # ranges  0.0-1.0
        ("mUnfilteredSteering", ctypes.c_double),             # ranges -1.0-1.0 (left to right)
        ("mUnfilteredClutch", ctypes.c_double),               # ranges  0.0-1.0
        ("mFilteredThrottle", ctypes.c_double),               # ranges  0.0-1.0
        ("mFilteredBrake", ctypes.c_double),                  # ranges  0.0-1.0
        ("mFilteredSteering", ctypes.c_double),               # ranges -1.0-1.0 (left to right)
        ("mFilteredClutch", ctypes.c_double),                 # ranges  0.0-1.0
        ("mSteeringShaftTorque", ctypes.c_double),            # torque around steering shaft (used to be mSteeringArmForce, but that is not necessarily accurate for feedback purposes)
        ("mFront3rdDeflection", ctypes.c_double),             # deflection at front 3rd spring
        ("mRear3rdDeflection", ctypes.c_double),              # deflection at rear 3rd spring
        ("mFrontWingHeight", ctypes.c_double),                # front wing height
        ("mFrontRideHeight", ctypes.c_double),                # front ride height
        ("mRearRideHeight", ctypes.c_double),                 # rear ride height
        ("mDrag", ctypes.c_double),                           # drag
        ("mFrontDownforce", ctypes.c_double),                 # front downforce
        ("mRearDownforce", ctypes.c_double),                  # rear downforce
        ("mFuel", ctypes.c_double),                           # amount of fuel (liters)
        ("mEngineMaxRPM", ctypes.c_double),                   # rev limit
        ("mScheduledStops", ctypes.c_ubyte),                  # number of scheduled pitstops
        ("mOverheating", ctypes.c_bool),                      # whether overheating icon is shown
        ("mDetached", ctypes.c_bool),                         # whether any parts (besides wheels) have been detached
        ("mHeadlights", ctypes.c_bool),                       # whether headlights are on
        ("mDentSeverity", ctypes.c_ubyte*8),                  # dent severity at 8 locations around the car (0=none, 1=some, 2=more)
        ("mLastImpactET", ctypes.c_double),                   # time of last impact
        ("mLastImpactMagnitude", ctypes.c_double),            # magnitude of last impact
        ("mLastImpactPos", LMUVect3),                         # location of last impact
        ("mEngineTorque", ctypes.c_double),                   # current engine torque (including additive torque) (used to be mEngineTq, but there's little reason to abbreviate it)
        ("mCurrentSector", ctypes.c_int),                     # the current sector (zero-based) with the pitlane stored in the sign bit (example: entering pits from third sector gives 0x80000002)
        ("mSpeedLimiter", ctypes.c_ubyte),                    # whether speed limiter is on
        ("mMaxGears", ctypes.c_ubyte),                        # maximum forward gears
        ("mFrontTireCompoundIndex", ctypes.c_ubyte),          # index within brand
        ("mRearTireCompoundIndex", ctypes.c_ubyte),           # index within brand
        ("mFuelCapacity", ctypes.c_double),                   # capacity in liters
        ("mFrontFlapActivated", ctypes.c_ubyte),              # whether front flap is activated
        ("mRearFlapActivated", ctypes.c_ubyte),               # whether rear flap is activated
        ("mRearFlapLegalStatus", ctypes.c_ubyte),             # 0=disallowed, 1=criteria detected but not allowed quite yet, 2 = allowed
        ("mIgnitionStarter", ctypes.c_ubyte),                 # 0=off 1=ignition 2 = ignition+starter
        ("mFrontTireCompoundName", ctypes.c_char*18),         # name of front tire compound
        ("mRearTireCompoundName", ctypes.c_char*18),          # name of rear tire compound
        ("mSpeedLimiterAvailable", ctypes.c_ubyte),           # whether speed limiter is available
        ("mAntiStallActivated", ctypes.c_ubyte),              # whether (hard) anti-stall is activated
        ("mUnused", ctypes.c_ubyte*2),
        ("mVisualSteeringWheelRange", ctypes.c_float),        # the *visual* steering wheel range
        ("mRearBrakeBias", ctypes.c_double),                  # fraction of brakes on rear
        ("mTurboBoostPressure", ctypes.c_double),             # current turbo boost pressure if available
        ("mPhysicsToGraphicsOffset", ctypes.c_float*3),       # offset from static CG to graphical center
        ("mPhysicalSteeringWheelRange", ctypes.c_float),      # the *physical* steering wheel range
        ("mDeltaBest", ctypes.c_double),                      # deltabest
        ("mBatteryChargeFraction", ctypes.c_double),          # Battery charge as fraction [0.0-1.0]
        ("mElectricBoostMotorTorque", ctypes.c_double),       # current torque of boost motor (can be negative when in regenerating mode)
        ("mElectricBoostMotorRPM", ctypes.c_double),          # current rpm of boost motor
        ("mElectricBoostMotorTemperature", ctypes.c_double),  # current temperature of boost motor
        ("mElectricBoostWaterTemperature", ctypes.c_double),  # current water temperature of boost motor cooler if present (0 otherwise)
        ("mElectricBoostMotorState", ctypes.c_ubyte),         # 0=unavailable 1=inactive, 2=propulsion, 3=regeneration
        ("mExpansion", ctypes.c_ubyte*(111-8)),               # for future use (note that the slot ID has been moved to mID above)
        ("mWheels", LMUWheel*4),                              # wheel info (0=front left, 1=front right, 2=rear left, 3=rear right)
    ]


class LMUVehicleScoring(ctypes.Structure):
    """Mapping of 'VehicleScoringInfoV01' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mID", ctypes.c_int),                   # slot ID (note that it can be re-used in multiplayer after someone leaves)
        ("mDriverName", ctypes.c_char*32),       # driver name
        ("mVehicleName", ctypes.c_char*64),      # vehicle name
        ("mTotalLaps", ctypes.c_short),          # laps completed
        ("mSector", ctypes.c_byte),              # 0=sector3, 1=sector1, 2 = sector2 (don't ask why)
        ("mFinishStatus", ctypes.c_byte),        # 0=none, 1=finished, 2=dnf, 3 = dq
        ("mLapDist", ctypes.c_double),           # current distance around track
        ("mPathLateral", ctypes.c_double),       # lateral position with respect to *very approximate* "center" path
        ("mTrackEdge", ctypes.c_double),         # track edge (w.r.t. "center" path) on same side of track as vehicle
        ("mBestSector1", ctypes.c_double),       # best sector 1
        ("mBestSector2", ctypes.c_double),       # best sector 2 (plus sector 1)
        ("mBestLapTime", ctypes.c_double),       # best lap time
        ("mLastSector1", ctypes.c_double),       # last sector 1
        ("mLastSector2", ctypes.c_double),       # last sector 2 (plus sector 1)
        ("mLastLapTime", ctypes.c_double),       # last lap time
        ("mCurSector1", ctypes.c_double),        # current sector 1 if valid
        ("mCurSector2", ctypes.c_double),        # current sector 2 (plus sector 1) if valid
        ("mNumPitstops", ctypes.c_short),        # number of pitstops made
        ("mNumPenalties", ctypes.c_short),       # number of outstanding penalties
        ("mIsPlayer", ctypes.c_bool),            # is this the player's vehicle
        ("mControl", ctypes.c_byte),             # who's in control: -1=nobody (shouldn't get this), 0=local player, 1=local AI, 2=remote, 3 = replay (shouldn't get this)
        ("mInPits", ctypes.c_bool),              # between pit entrance and pit exit (not always accurate for remote vehicles)
        ("mPlace", ctypes.c_ubyte),              # 1-based position
        ("mVehicleClass", ctypes.c_char*32),     # vehicle class
        ("mTimeBehindNext", ctypes.c_double),    # time behind vehicle in next higher place
        ("mLapsBehindNext", ctypes.c_int),       # laps behind vehicle in next higher place
        ("mTimeBehindLeader", ctypes.c_double),  # time behind leader
        ("mLapsBehindLeader", ctypes.c_int),     # laps behind leader
        ("mLapStartET", ctypes.c_double),        # time this lap was started
        ("mPos", LMUVect3),                      # world position in meters
        ("mLocalVel", LMUVect3),                 # velocity (meters/sec) in local vehicle coordinates
        ("mLocalAccel", LMUVect3),               # acceleration (meters/sec^2) in local vehicle coordinates
        ("mOri", LMUVect3*3),                    # rows of orientation matrix (use TelemQuat conversions if desired), also converts local
        ("mLocalRot", LMUVect3),                 # rotation (radians/sec) in local vehicle coordinates
        ("mLocalRotAccel", LMUVect3),            # rotational acceleration (radians/sec^2) in local vehicle coordinates
        ("mHeadlights", ctypes.c_ubyte),         # status of headlights
        ("mPitState", ctypes.c_ubyte),           # 0=none, 1=request, 2=entering, 3=stopped, 4=exiting
        ("mServerScored", ctypes.c_ubyte),       # whether this vehicle is being scored by server (could be off in qualifying or racing heats)
        ("mIndividualPhase", ctypes.c_ubyte),    # game phases (described below) plus 9=after formation, 10=under yellow, 11 = under blue (not used)
        ("mQualification", ctypes.c_int),        # 1-based, can be -1 when invalid
        ("mTimeIntoLap", ctypes.c_double),       # estimated time into lap
        ("mEstimatedLapTime", ctypes.c_double),  # estimated laptime used for "time behind" and "time into lap" (note: this may changed based on vehicle and setup!?)
        ("mPitGroup", ctypes.c_char*24),         # pit group (same as team name unless pit is shared)
        ("mFlag", ctypes.c_ubyte),               # primary flag being shown to vehicle (currently only 0=green or 6 = blue)
        ("mUnderYellow", ctypes.c_bool),         # whether this car has taken a full-course caution flag at the start/finish line
        ("mCountLapFlag", ctypes.c_ubyte),       # 0 = do not count lap or time, 1 = count lap but not time, 2 = count lap and time
        ("mInGarageStall", ctypes.c_bool),       # appears to be within the correct garage stall
        ("mUpgradePack", ctypes.c_ubyte*16),     # Coded upgrades
        ("mPitLapDist", ctypes.c_float),         # location of pit in terms of lap distance
        ("mBestLapSector1", ctypes.c_float),     # sector 1 time from best lap (not necessarily the best sector 1 time)
        ("mBestLapSector2", ctypes.c_float),     # sector 2 time from best lap (not necessarily the best sector 2 time)
        ("mSteamID", ctypes.c_ulonglong),        # SteamID of the current driver (if any)
        ("mVehFilename", ctypes.c_char*32),      # filename of veh file used to identify this vehicle.
        ("mAttackMode", ctypes.c_short),
        # 2020.11.12 - Took 1 byte from mExpansion to transmit fuel percentage
        ("mFuelFraction", ctypes.c_ubyte),       # Percentage of fuel or battery left in vehicle. 0x00 = 0%; 0xFF = 100%
        # 2021.05.28 - Took 1 byte from mExpansion to transmit DRS (RearFlap) state - consider making this a bitfield if further bools are needed later on
        ("mDRSState", ctypes.c_bool),
        ("mExpansion", ctypes.c_ubyte*4),        # for future use
    ]


class LMUScoringInfo(ctypes.Structure):
    """Mapping of 'ScoringInfoV01' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mTrackName", ctypes.c_char*64),         # current track name
        ("mSession", ctypes.c_int),               # current session (0=testday 1-4=practice 5-8=qual 9=warmup 10-13=race)
        ("mCurrentET", ctypes.c_double),          # current time
        ("mEndET", ctypes.c_double),              # ending time
        ("mMaxLaps", ctypes.c_int),               # maximum laps
        ("mLapDist", ctypes.c_double),            # distance around track
        ("mResultsStreamPointer", ctypes.c_ubyte*8),     # (pointer) results stream additions since last update (newline-delimited and NULL-terminated)
        ("mNumVehicles", ctypes.c_int),           # current number of vehicles
        # Game phases:
        # 0 Before session has begun
        # 1 Reconnaissance laps (race only)
        # 2 Grid walk-through (race only)
        # 3 Formation lap (race only)
        # 4 Starting-light countdown has begun (race only)
        # 5 Green flag
        # 6 Full course yellow / safety car
        # 7 Session stopped
        # 8 Session over
        # 9 Paused (tag.2015.09.14 - this is new, and indicates that this is a heartbeat call to the plugin)
        ("mGamePhase", ctypes.c_ubyte),
        # Yellow flag states (applies to full-course only)
        # -1 Invalid
        #  0 None
        #  1 Pending
        #  2 Pits closed
        #  3 Pit lead lap
        #  4 Pits open
        #  5 Last lap
        #  6 Resume
        #  7 Race halt (not currently used)
        ("mYellowFlagState", ctypes.c_char),
        ("mSectorFlag", ctypes.c_ubyte*3),        # whether there are any local yellows at the moment in each sector (not sure if sector 0 is first or last, so test)
        ("mStartLight", ctypes.c_ubyte),          # start light frame (number depends on track)
        ("mNumRedLights", ctypes.c_ubyte),        # number of red lights in start sequence
        ("mInRealtime", ctypes.c_bool),           # in realtime as opposed to at the monitor
        ("mPlayerName", ctypes.c_char*32),        # player name (including possible multiplayer override)
        ("mPlrFileName", ctypes.c_char*64),       # may be encoded to be a legal filename
        ("mDarkCloud", ctypes.c_double),          # cloud darkness? 0.0-1.0
        ("mRaining", ctypes.c_double),            # raining severity 0.0-1.0
        ("mAmbientTemp", ctypes.c_double),        # temperature (Celsius)
        ("mTrackTemp", ctypes.c_double),          # temperature (Celsius)
        ("mWind", LMUVect3),                      # wind speed
        ("mMinPathWetness", ctypes.c_double),     # minimum wetness on main path 0.0-1.0
        ("mMaxPathWetness", ctypes.c_double),     # maximum wetness on main path 0.0-1.0
        ("mGameMode", ctypes.c_ubyte),            # 1 = server, 2 = client, 3 = server and client
        ("mIsPasswordProtected", ctypes.c_bool),  # is the server password protected
        ("mServerPort", ctypes.c_ushort),         # the port of the server (if on a server)
        ("mServerPublicIP", ctypes.c_uint),       # the public IP address of the server (if on a server)
        ("mMaxPlayers", ctypes.c_int),            # maximum number of vehicles that can be in the session
        ("mServerName", ctypes.c_char*32),        # name of the server
        ("mStartET", ctypes.c_float),             # start time (seconds since midnight) of the event
        ("mAvgPathWetness", ctypes.c_double),     # average wetness on main path 0.0-1.0
        ("mExpansion", ctypes.c_ubyte*200),       # future use
        ("mVehiclePointer", ctypes.c_ubyte*8),    # (pointer) keeping this at the end of the structure to make it easier to replace in future versions
    ]


class LMUApplicationState(ctypes.Structure):
    """Mapping of 'ApplicationStateV01' from InternalsPlugin.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("mAppWindow", ctypes.c_ulonglong),    # HWND, application window handle
        ("mWidth", ctypes.c_uint),             # screen width
        ("mHeight", ctypes.c_uint),            # screen height
        ("mRefreshRate", ctypes.c_uint),       # refresh rate
        ("mWindowed", ctypes.c_uint),          # really just a boolean whether we are in windowed mode
        ("mOptionsLocation", ctypes.c_ubyte),  # 0=main UI, 1=track loading, 2=monitor, 3=on track
        ("mOptionsPage", ctypes.c_char*31),    # the name of the options page
        ("mExpansion", ctypes.c_ubyte*204),    # future use
    ]


# SharedMemoryInterface

class LMUScoringData(ctypes.Structure):
    """Mapping of 'SharedMemoryScoringData' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("scoringInfo", LMUScoringInfo),
        ("scoringStreamSize", ctypes.c_ubyte*12),
        ("vehScoringInfo", LMUVehicleScoring*LMUConstants.MAX_MAPPED_VEHICLES),
        ("scoringStream", ctypes.c_char*65536),
    ]


class LMUTelemetryData(ctypes.Structure):
    """Mapping of 'SharedMemoryTelemtryData' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("activeVehicles", ctypes.c_uint8),
        ("playerVehicleIdx", ctypes.c_uint8),
        ("playerHasVehicle", ctypes.c_bool),
        ("telemInfo", LMUVehicleTelemetry*LMUConstants.MAX_MAPPED_VEHICLES),
    ]


class LMUPathData(ctypes.Structure):
    """Mapping of 'SharedMemoryPathData' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("userData", ctypes.c_char*LMUConstants.MAX_PATH_LENGTH),
        ("customVariables", ctypes.c_char*LMUConstants.MAX_PATH_LENGTH),
        ("stewardResults", ctypes.c_char*LMUConstants.MAX_PATH_LENGTH),
        ("playerProfile", ctypes.c_char*LMUConstants.MAX_PATH_LENGTH),
        ("pluginsFolder", ctypes.c_char*LMUConstants.MAX_PATH_LENGTH),
    ]


class LMUEvent(ctypes.Structure):
    """Remapping of 'SharedMemoryEvent' enum as struct from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("SME_ENTER", ctypes.c_uint),
        ("SME_EXIT", ctypes.c_uint),
        ("SME_STARTUP", ctypes.c_uint),
        ("SME_SHUTDOWN", ctypes.c_uint),
        ("SME_LOAD", ctypes.c_uint),
        ("SME_UNLOAD", ctypes.c_uint),
        ("SME_START_SESSION", ctypes.c_uint),
        ("SME_END_SESSION", ctypes.c_uint),
        ("SME_ENTER_REALTIME", ctypes.c_uint),
        ("SME_EXIT_REALTIME", ctypes.c_uint),
        ("SME_UPDATE_SCORING", ctypes.c_uint),
        ("SME_UPDATE_TELEMETRY", ctypes.c_uint),
        ("SME_INIT_APPLICATION", ctypes.c_uint),
        ("SME_UNINIT_APPLICATION", ctypes.c_uint),
        ("SME_SET_ENVIRONMENT", ctypes.c_uint),
        ("SME_FFB", ctypes.c_uint),
        # omit "SME_MAX"
    ]


class LMUGeneric(ctypes.Structure):
    """Mapping of 'SharedMemoryGeneric' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("events", LMUEvent),
        ("gameVersion", ctypes.c_int),
        ("FFBTorque", ctypes.c_float),
        ("appInfo", LMUApplicationState),
    ]


class LMUObjectOut(ctypes.Structure):
    """Mapping of 'SharedMemoryObjectOut' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("generic", LMUGeneric),
        ("paths", LMUPathData),
        ("scoring", LMUScoringData),
        ("telemetry", LMUTelemetryData),
    ]


class LMULayout(ctypes.Structure):
    """Mapping of 'SharedMemoryLayout' from SharedMemoryInterface.hpp"""

    __slots__ = ()
    _pack_ = 4
    _fields_ = [
        ("data", LMUObjectOut),
    ]


# Memory map

class SimInfo:
    """Simulation info from shared memory"""

    def __init__(self):
        self._lmu_data = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(LMUObjectOut),
            tagname=LMUConstants.LMU_SHARED_MEMORY_FILE,
        )
        self.LMUData = LMUObjectOut.from_buffer(self._lmu_data)

    def save(self, filename: str):
        """Save buffer data to file"""
        with open(filename, "wb") as output:
            output.write(bytes(self._lmu_data))

    def close(self):
        """Close memory map"""
        self.LMUData = None

        try:  # this did not help with the errors
            self._lmu_data.close()
        except BufferError as e:
            print("Error:", e)

    def __del__(self):
        self.close()


def test():
    """Example usage"""
    info = SimInfo()

    # Uncomment to save raw memory data to file
    # info.save("LMU_SHARED_MEMORY_FILE.txt")

    generic_data = info.LMUData.generic
    scor_data = info.LMUData.scoring
    tele_data = info.LMUData.telemetry

    player_index = tele_data.playerVehicleIdx
    selected_player_index = 0

    player_scor_data = scor_data.vehScoringInfo[selected_player_index]
    player_tele_data = tele_data.telemInfo[selected_player_index]

    print("-"*40)
    print("Game info:")
    print("Version:", generic_data.gameVersion)
    print("FFB torque:", generic_data.FFBTorque)
    print("HWND:", generic_data.appInfo.mAppWindow)
    print("Screen width:", generic_data.appInfo.mWidth)
    print("Screen height:", generic_data.appInfo.mHeight)
    print("Refresh rate:", generic_data.appInfo.mRefreshRate)
    print("Options location:", generic_data.appInfo.mOptionsLocation)
    print("Options page:", generic_data.appInfo.mOptionsPage)

    print("-"*40)
    print("Path info:")
    print("User data:", info.LMUData.paths.userData)
    print("Custom variables:", info.LMUData.paths.customVariables)
    print("Steward results:", info.LMUData.paths.stewardResults)
    print("Player profile:", info.LMUData.paths.playerProfile)
    print("Plugins folder:", info.LMUData.paths.pluginsFolder)

    print("-"*40)
    print("Scoring info:")
    print("Track name:", scor_data.scoringInfo.mTrackName)
    print("Local player name:", scor_data.scoringInfo.mPlayerName)
    print("Local player index:", player_index)
    print("Setting name:", scor_data.scoringInfo.mPlrFileName)
    print("Total vehicles:", scor_data.scoringInfo.mNumVehicles)

    print("-"*40)
    print("Selected Player scoring info:")
    print("Slot ID:", player_scor_data.mID)
    print("Driver name:", player_scor_data.mDriverName)
    print("VEH file:", player_scor_data.mVehFilename)
    print("Is local player:", player_scor_data.mIsPlayer)

    print("-"*40)
    print("Selected player telemetry info:")
    print("Slot ID:", player_tele_data.mID)
    print("Vehicle:", player_tele_data.mVehicleName)
    print("Gear:", player_tele_data.mGear)
    print("Throttle:", player_tele_data.mUnfilteredThrottle)
    print("Brake:", player_tele_data.mUnfilteredBrake)
    print("Clutch:", player_tele_data.mUnfilteredClutch)

    print("-"*40)
    print("Event Info")
    print("SME_ENTER:", generic_data.events.SME_ENTER)
    print("SME_EXIT:", generic_data.events.SME_EXIT)
    print("SME_SET_ENVIRONMENT:", generic_data.events.SME_SET_ENVIRONMENT)
    print("SME_UPDATE_SCORING:", generic_data.events.SME_UPDATE_SCORING)
    print("SME_UPDATE_TELEMETRY:", generic_data.events.SME_UPDATE_TELEMETRY)

    player_scor_data = None
    player_tele_data = None
    generic_data = None
    scor_data = None
    tele_data = None


if __name__ == "__main__":
    test()
