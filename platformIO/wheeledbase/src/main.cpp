#include <Arduino.h>

#include "PIN.h"
#include "constants.h"
#include "instructions.h"
#include "addresses.h"

#include "SerialTalking.h"
#include "DCMotor.h"
#include "Codewheel.h"
#include "Odometry.h"
#include "PID.h"
#include "VelocityController.h"
#include "PositionController.h"
#include "PurePursuit.h"
#include "TurnOnTheSpot.h"
#include "mathutils.h"

// Load the different modules

DCMotorsDriver driver;
DCMotor leftWheel;
DCMotor rightWheel;

Codewheel leftCodewheel;
Codewheel rightCodewheel;

Odometry odometry;

VelocityController velocityControl;
#if ENABLE_VELOCITYCONTROLLER_LOGS
VelocityControllerLogs controllerLogs;
#endif // ENABLE_VELOCITYCONTROLLER_LOGS

PID linVelPID;
PID angVelPID;

PositionController positionControl;

PurePursuit purePursuit;
TurnOnTheSpot turnOnTheSpot;

// Setup

void setup(){
    // Communication
    Serial.begin(SERIALTALKING_BAUDRATE);
    talking.begin(Serial);
    talking.bind(SET_OPENLOOP_VELOCITIES_OPCODE, SET_OPENLOOP_VELOCITIES);
    talking.bind(GET_CODEWHEELS_COUNTERS_OPCODE, GET_CODEWHEELS_COUNTERS);
    talking.bind(SET_VELOCITIES_OPCODE, SET_VELOCITIES);
    talking.bind(RESET_PUREPURSUIT_OPCODE, RESET_PUREPURSUIT);
    talking.bind(ADD_PUREPURSUIT_WAYPOINT_OPCODE, ADD_PUREPURSUIT_WAYPOINT);
    talking.bind(START_PUREPURSUIT_OPCODE, START_PUREPURSUIT);
    talking.bind(START_TURNONTHESPOT_OPCODE, START_TURNONTHESPOT);
    talking.bind(POSITION_REACHED_OPCODE, POSITION_REACHED);
    talking.bind(SET_POSITION_OPCODE, SET_POSITION);
    talking.bind(GET_POSITION_OPCODE, GET_POSITION);
    talking.bind(GET_VELOCITIES_OPCODE, GET_VELOCITIES);
    talking.bind(SET_PARAMETER_VALUE_OPCODE, SET_PARAMETER_VALUE);
    talking.bind(GET_PARAMETER_VALUE_OPCODE, GET_PARAMETER_VALUE);
    talking.bind(RESET_PARAMETERS_OPCODE, RESET_PARAMETERS);
    talking.bind(GET_VELOCITIES_WANTED_OPCODE, GET_VELOCITIES_WANTED);
    talking.bind(GOTO_DELTA_OPCODE, GOTO_DELTA);
    //talking.bind(SERIALTALKS_DISCONNECT_OPCODE, DISABLE);
    talking.bind(RESET_PARAMETERS_OPCODE, RESET_PARAMETERS);
    talking.bind(SAVE_PARAMETERS_OPCODE, SAVE_PARAMETERS);
    talking.bind(START_TURNONTHESPOT_DIR_OPCODE, START_TURNONTHESPOT_DIR);
    // DC motors wheels
    driver.attach(DRIVER_RESET, DRIVER_FAULT);
    driver.reset();

    leftWheel.attach(LEFT_MOTOR_EN, LEFT_MOTOR_PWM, LEFT_MOTOR_DIR);
    rightWheel.attach(RIGHT_MOTOR_EN, RIGHT_MOTOR_PWM, RIGHT_MOTOR_DIR);
    leftWheel.load(LEFTWHEEL_ADDRESS);
    rightWheel.load(RIGHTWHEEL_ADDRESS);
    //settings for EEPROM
    leftWheel.setWheelRadius(LEFT_WHEEL_RADIUS);
    rightWheel.setWheelRadius(RIGHT_WHEEL_RADIUS);
    leftWheel.setConstant(DCMOTORS_VELOCITY_CONSTANT);
    rightWheel.setConstant(DCMOTORS_VELOCITY_CONSTANT);
    //leftWheel.setMaxPWM(); <- pas trouvé de valeur
    //rightWheel.setMaxPWM(); <- pas trouvé de valeur
    leftWheel.save(LEFTWHEEL_ADDRESS);
    rightWheel.save(RIGHTWHEEL_ADDRESS);

    // Codewheels
    leftCodewheel.attachCounter(QUAD_COUNTER_XY, QUAD_COUNTER_Y_AXIS, QUAD_COUNTER_SEL1, QUAD_COUNTER_SEL2, QUAD_COUNTER_OE, QUAD_COUNTER_RST_Y);
    rightCodewheel.attachCounter(QUAD_COUNTER_XY, QUAD_COUNTER_X_AXIS, QUAD_COUNTER_SEL1, QUAD_COUNTER_SEL2, QUAD_COUNTER_OE, QUAD_COUNTER_RST_X);
    leftCodewheel.attachRegister(SHIFT_REG_DATA, SHIFT_REG_LATCH, SHIFT_REG_CLOCK);
    rightCodewheel.attachRegister(SHIFT_REG_DATA, SHIFT_REG_LATCH, SHIFT_REG_CLOCK);
    leftCodewheel.load(LEFTCODEWHEEL_ADDRESS);
    rightCodewheel.load(RIGHTCODEWHEEL_ADDRESS);
    leftCodewheel.reset();
    rightCodewheel.reset();
    //settings for EEPROM
    leftCodewheel.setWheelRadius(LEFT_CODEWHEEL_RADIUS);
    rightCodewheel.setWheelRadius(RIGHT_CODEWHEEL_RADIUS);
    leftCodewheel.setCountsPerRev(CODEWHEELS_COUNTS_PER_REVOLUTION);
    rightCodewheel.setCountsPerRev(CODEWHEELS_COUNTS_PER_REVOLUTION);
    leftCodewheel.save(LEFTCODEWHEEL_ADDRESS);
    rightCodewheel.save(RIGHTCODEWHEEL_ADDRESS);

    // Odometry
    odometry.load(ODOMETRY_ADDRESS);
    odometry.setCodewheels(leftCodewheel, rightCodewheel);
    odometry.setTimestep(ODOMETRY_TIMESTEP);
    odometry.enable();
    //settings for EEPROM
    odometry.setAxleTrack(CODEWHEELS_AXLE_TRACK);
    //odometry.setSlippage(); <- pas trouvé de valeur
    odometry.save(ODOMETRY_ADDRESS);


    // Engineering control
    velocityControl.load(VELOCITYCONTROL_ADDRESS);
    velocityControl.setWheels(leftWheel, rightWheel);
    velocityControl.setPID(linVelPID, angVelPID);
    velocityControl.disable();
    //settings for EEPROM
    velocityControl.setMaxAngAcc(MAX_ANGULAR_ACCELERATION);
    velocityControl.setMaxAngDec(MAX_ANGULAR_DECCELERATION);
    velocityControl.setMaxLinAcc(MAX_LINEAR_ACCELERATION);
    velocityControl.setMaxLinDec(MAX_LINEAR_DECCELERATION);
    //velocityControl.setSpinShutdown(); <- pas trouvé de valeur
    velocityControl.save(VELOCITYCONTROL_ADDRESS);

    //const float maxLinVel = min(leftWheel.getMaxVelocity(), rightWheel.getMaxVelocity());
    //const float maxAngVel = min(leftWheel.getMaxVelocity(), rightWheel.getMaxVelocity()) * 2 / WHEELS_AXLE_TRACK;
    linVelPID.load(LINVELPID_ADDRESS);
    angVelPID.load(ANGVELPID_ADDRESS);
    //linVelPID.setOutputLimits(-maxLinVel, maxLinVel);
    //angVelPID.setOutputLimits(-maxAngVel, maxAngVel);

#if ENABLE_VELOCITYCONTROLLER_LOGS
    controllerLogs.setController(velocityControl);
    controllerLogs.setTimestep(VELOCITYCONTROLLER_LOGS_TIMESTEP);
    controllerLogs.enable();
#endif // VELOCITYENABLE_CONTROLLER_LOGS

    // Position control
    positionControl.load(POSITIONCONTROL_ADDRESS);
    positionControl.setTimestep(POSITIONCONTROL_TIMESTEP);
    positionControl.disable();

    purePursuit.load(PUREPURSUIT_ADDRESS);

    // Miscellanous
    TCCR2B = (TCCR2B & 0b11111000) | 1; // Set Timer2 frequency to 16MHz instead of 250kHz
}

// Loop

void loop()
{
    talking.execute();

    // Update odometry
    if (odometry.update())
    {
        positionControl.setPosInput(odometry.getPosition());
        velocityControl.setInputs(odometry.getLinVel(), odometry.getAngVel());
    }

    // Compute trajectory
    if (positionControl.update())
    {
        float linVelSetpoint = positionControl.getLinVelSetpoint();
        float angVelSetpoint = positionControl.getAngVelSetpoint();
        velocityControl.setSetpoints(linVelSetpoint, angVelSetpoint);
    }

    // Integrate engineering control
#if ENABLE_VELOCITYCONTROLLER_LOGS
    if (velocityControl.update())
        controllerLogs.update();
#else
    velocityControl.update();
#endif // ENABLE_VELOCITYCONTROLLER_LOGS
}
