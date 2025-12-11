"""
LMU API data type hints & annotation

Helper classes with type hints & annotation reference to lmu_data.py for IDE & type checker.

Annotate "ctypes type" as "Python type" according to table from:
https://docs.python.org/3/library/ctypes.html#fundamental-data-types

Annotate array object as tuple[type, ...] to specify number of elements contained.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class _NOINIT(ABC):
    """Disable instantiate"""

    @abstractmethod
    def _(self): ...


class LMUVect3(_NOINIT):
    x: float
    y: float
    z: float


class LMUWheel(_NOINIT):
    mSuspensionDeflection: float
    mRideHeight: float
    mSuspForce: float
    mBrakeTemp: float
    mBrakePressure: float
    mRotation: float
    mLateralPatchVel: float
    mLongitudinalPatchVel: float
    mLateralGroundVel: float
    mLongitudinalGroundVel: float
    mCamber: float
    mLateralForce: float
    mLongitudinalForce: float
    mTireLoad: float
    mGripFract: float
    mPressure: float
    mTemperature: tuple[float, float, float]
    mWear: float
    mTerrainName: bytes
    mSurfaceType: int
    mFlat: bool
    mDetached: bool
    mStaticUndeflectedRadius: int
    mVerticalTireDeflection: float
    mWheelYLocation: float
    mToe: float
    mTireCarcassTemperature: float
    mTireInnerLayerTemperature: tuple[float, float, float]
    mExpansion: tuple[int, ...]


class LMUVehicleTelemetry(_NOINIT):
    mID: int
    mDeltaTime: float
    mElapsedTime: float
    mLapNumber: int
    mLapStartET: float
    mVehicleName: bytes
    mTrackName: bytes
    mPos: LMUVect3
    mLocalVel: LMUVect3
    mLocalAccel: LMUVect3
    mOri: tuple[LMUVect3, LMUVect3, LMUVect3]
    mLocalRot: LMUVect3
    mLocalRotAccel: LMUVect3
    mGear: int
    mEngineRPM: float
    mEngineWaterTemp: float
    mEngineOilTemp: float
    mClutchRPM: float
    mUnfilteredThrottle: float
    mUnfilteredBrake: float
    mUnfilteredSteering: float
    mUnfilteredClutch: float
    mFilteredThrottle: float
    mFilteredBrake: float
    mFilteredSteering: float
    mFilteredClutch: float
    mSteeringShaftTorque: float
    mFront3rdDeflection: float
    mRear3rdDeflection: float
    mFrontWingHeight: float
    mFrontRideHeight: float
    mRearRideHeight: float
    mDrag: float
    mFrontDownforce: float
    mRearDownforce: float
    mFuel: float
    mEngineMaxRPM: float
    mScheduledStops: int
    mOverheating: bool
    mDetached: bool
    mHeadlights: bool
    mDentSeverity: tuple[int, int, int, int, int, int, int, int]
    mLastImpactET: float
    mLastImpactMagnitude: float
    mLastImpactPos: LMUVect3
    mEngineTorque: float
    mCurrentSector: int
    mSpeedLimiter: int
    mMaxGears: int
    mFrontTireCompoundIndex: int
    mRearTireCompoundIndex: int
    mFuelCapacity: float
    mFrontFlapActivated: int
    mRearFlapActivated: int
    mRearFlapLegalStatus: int
    mIgnitionStarter: int
    mFrontTireCompoundName: bytes
    mRearTireCompoundName: bytes
    mSpeedLimiterAvailable: int
    mAntiStallActivated: int
    mUnused: tuple[int, int]
    mVisualSteeringWheelRange: float
    mRearBrakeBias: float
    mTurboBoostPressure: float
    mPhysicsToGraphicsOffset: tuple[float, float, float]
    mPhysicalSteeringWheelRange: float
    mDeltaBest: float
    mBatteryChargeFraction: float
    mElectricBoostMotorTorque: float
    mElectricBoostMotorRPM: float
    mElectricBoostMotorTemperature: float
    mElectricBoostWaterTemperature: float
    mElectricBoostMotorState: int
    mExpansion: tuple[int, ...]
    mWheels: tuple[LMUWheel, LMUWheel, LMUWheel, LMUWheel]


class LMUVehicleScoring(_NOINIT):
    mID: int
    mDriverName: bytes
    mVehicleName: bytes
    mTotalLaps: int
    mSector: int
    mFinishStatus: int
    mLapDist: float
    mPathLateral: float
    mTrackEdge: float
    mBestSector1: float
    mBestSector2: float
    mBestLapTime: float
    mLastSector1: float
    mLastSector2: float
    mLastLapTime: float
    mCurSector1: float
    mCurSector2: float
    mNumPitstops: int
    mNumPenalties: int
    mIsPlayer: bool
    mControl: int
    mInPits: bool
    mPlace: int
    mVehicleClass: bytes
    mTimeBehindNext: float
    mLapsBehindNext: int
    mTimeBehindLeader: float
    mLapsBehindLeader: int
    mLapStartET: float
    mPos: LMUVect3
    mLocalVel: LMUVect3
    mLocalAccel: LMUVect3
    mOri: tuple[LMUVect3, LMUVect3, LMUVect3]
    mLocalRot: LMUVect3
    mLocalRotAccel: LMUVect3
    mHeadlights: int
    mPitState: int
    mServerScored: int
    mIndividualPhase: int
    mQualification: int
    mTimeIntoLap: float
    mEstimatedLapTime: float
    mPitGroup: bytes
    mFlag: int
    mUnderYellow: bool
    mCountLapFlag: int
    mInGarageStall: bool
    mUpgradePack: tuple[int, ...]
    mPitLapDist: float
    mBestLapSector1: float
    mBestLapSector2: float
    mSteamID: int
    mVehFilename: str
    mAttackMode: int
    mFuelFraction: float
    mDRSState: bool
    mExpansion: tuple[int, ...]


class LMUScoringInfo(_NOINIT):
    mTrackName: bytes
    mSession: int
    mCurrentET: float
    mEndET: float
    mMaxLaps: int
    mLapDist: float
    pointer1: tuple[int, ...]
    mNumVehicles: int
    mGamePhase: int
    mYellowFlagState: int
    mSectorFlag: tuple[int, int, int]
    mStartLight: int
    mNumRedLights: int
    mInRealtime: bool
    mPlayerName: bytes
    mPlrFileName: bytes
    mDarkCloud: float
    mRaining: float
    mAmbientTemp: float
    mTrackTemp: float
    mWind: LMUVect3
    mMinPathWetness: float
    mMaxPathWetness: float
    mGameMode: int
    mIsPasswordProtected: bool
    mServerPort: int
    mServerPublicIP: int
    mMaxPlayers: int
    mServerName: bytes
    mStartET: float
    mAvgPathWetness: float
    mExpansion: tuple[int, ...]
    pointer2: tuple[int, ...]


class LMUApplicationState(_NOINIT):
    mAppWindow: int
    mWidth: int
    mHeight: int
    mRefreshRate: int
    mWindowed: int
    mOptionsLocation: int
    mOptionsPage: str
    mExpansion: tuple[int, ...]


class LMUScoringData(_NOINIT):
    scoringInfo: LMUScoringInfo
    scoringStreamSize: int
    vehScoringInfo: tuple[LMUVehicleScoring, ...]
    scoringStream: str


class LMUTelemetryData(_NOINIT):
    activeVehicles: int
    playerVehicleIdx: int
    playerHasVehicle: bool
    telemInfo: tuple[LMUVehicleTelemetry, ...]


class LMUPathData(_NOINIT):
    userData: str
    customVariables: str
    stewardResults: str
    playerProfile: str
    pluginsFolder: str


class LMUEvent(_NOINIT):
    SME_ENTER: int
    SME_EXIT: int
    SME_STARTUP: int
    SME_SHUTDOWN: int
    SME_LOAD: int
    SME_UNLOAD: int
    SME_START_SESSION: int
    SME_END_SESSION: int
    SME_ENTER_REALTIME: int
    SME_EXIT_REALTIME: int
    SME_UPDATE_SCORING: int
    SME_UPDATE_TELEMETRY: int
    SME_INIT_APPLICATION: int
    SME_UNINIT_APPLICATION: int
    SME_SET_ENVIRONMENT: int
    SME_FFB: int


class LMUGeneric(_NOINIT):
    events: LMUEvent
    gameVersion: int
    FFBTorque: float
    appInfo: LMUApplicationState


class LMUObjectOut(_NOINIT):
    generic: LMUGeneric
    paths: LMUPathData
    scoring: LMUScoringData
    telemetry: LMUTelemetryData


class LMULayout(_NOINIT):
    data: LMUObjectOut
