#!/usr/bin/python3

import serial
import time
import random
import math

def CheckSum(*args):
    hash = 0
    for a in args:
        hash = (hash + a)

    return ~hash & 0xff

def ServoMoveTimeWrite(id, angle, time):
    angle_upper, angle_lower = angle.to_bytes(2)
    time_upper, time_lower = time.to_bytes(2)

    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 1
    ba[5] = angle_lower 
    ba[6] = angle_upper 
    ba[7] = time_lower
    ba[8] = time_upper
    ba[9] = CheckSum(id, 7, 1, angle_upper, angle_lower, time_upper, time_lower)
    return ba;

def ServoMoveTimeRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 2
    ba[5] = CheckSum(id, 3, 2)
    return ba;

def ServoMoveTimeWaitWrite(id, angle, time):
    angle_upper, angle_lower = angle.to_bytes(2)
    time_upper, time_lower = time.to_bytes(2)

    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 7
    ba[5] = angle_lower 
    ba[6] = angle_upper 
    ba[7] = time_lower
    ba[8] = time_upper
    ba[9] = CheckSum(id, 7, 7, angle_upper, angle_lower, time_upper, time_lower)
    return ba;

def ServoMoveTimeWaitRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 8
    ba[5] = CheckSum(id, 3, 8)
    return ba;

def ServoMoveStart(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 11
    ba[5] = CheckSum(id, 3, 11)
    return ba;

def ServoMoveStop(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 12
    ba[5] = CheckSum(id, 3, 12)
    return ba;

def ServoIDWrite(id, newID):
    ba = bytearray(7)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 4
    ba[4] = 13
    ba[5] = newID & 0xff
    ba[6] = CheckSum(id, 4, 13, newID & 0xff)
    return ba;

def ServoIDRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 14
    ba[5] = CheckSum(id, 3, 14)
    return ba;

def ServoAngleOffsetAdjust(id, offset):
    ba = bytearray(7)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 4
    ba[4] = 17
    ba[5] = offset & 0xff
    ba[6] = CheckSum(id, 4, 17, offset & 0xff)
    return ba;

def ServoAngleOffsetSave(id, offset):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 18
    ba[5] = CheckSum(id, 3, 18)
    return ba;

def ServoAngleOffsetRead(id):
    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 9
    ba[5] = 0 
    ba[6] = 0 
    ba[7] = 0
    ba[8] = 0
    ba[9] = CheckSum(id, 9, 7)
    return ba;

def ServoAngleLimitWrite(id, angleMin, angleMax):
    angleMin_upper, angleMin_lower = angleMin.to_bytes(2)
    angleMax_upper, angleMax_lower = angleMax.to_bytes(2)

    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 20
    ba[5] = angleMin_lower 
    ba[6] = angleMin_upper 
    ba[7] = angleMax_lower
    ba[8] = angleMax_upper
    ba[9] = CheckSum(id, 20 , 7, angleMin_lower, angleMin_upper, angleMax_lower, angleMax_upper)
    return ba;

def ServoAngleLimitRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 21
    ba[5] = CheckSum(id, 3, 21)
    return ba;

def ServoVinLimitWrite(id, vin_min, vin_max):
    vinMin_upper, vinMin_lower = vin_min.to_bytes(2)
    vinMax_upper, vinMax_lower = vin_max.to_bytes(2)
    
    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 22
    ba[5] = vinMin_lower
    ba[6] = vinMin_upper
    ba[7] = vinMax_lower
    ba[8] = vinMax_upper
    ba[9] = CheckSum(id, 7, 21, vinMin_upper, vinMin_lower, vinMax_upper, vinMax_lower)
    return ba;

def ServoVinLimitRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 23
    ba[5] = CheckSum(id, 3, 23)
    return ba;

def ServoTempMaxLimitWrite(id, maxT):
    ba = bytearray(7)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 4
    ba[4] = 24
    ba[5] = maxT & 0xff
    ba[6] = CheckSum(id, 3, 24, maxT & 0xff)
    return ba;

def ServoTempMaxLimitRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 25
    ba[5] = CheckSum(id, 3, 25)
    return ba;

def ServoTempRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 26
    ba[5] = CheckSum(id, 3, 26)
    return ba;

def ServoVinRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 27
    ba[5] = CheckSum(id, 3, 27)
    return ba;

def ServoPosRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 28
    ba[5] = CheckSum(id, 3, 28)
    return ba;

def ServoModeWrite(id, mode, rate = 0):
    rate_upper, rate_lower = rate.to_bytes(2)
    
    ba = bytearray(10)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 7
    ba[4] = 29
    ba[5] = mode
    ba[6] = 0
    ba[7] = rate_lower
    ba[8] = rate_upper
    ba[9] = CheckSum(id, 7, 29, mode, rate_lower, rate_upper)
    return ba;

def ServoModeRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 30
    ba[5] = CheckSum(id, 3, 30)
    return ba;

def ServoLoadOrUnloadWrite(id, load):
    ba = bytearray(7)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 4
    ba[4] = 31
    ba[5] = load & 0x01
    ba[6] = CheckSum(id, 4, 31, load & 0x01)
    return ba;

def ServoLoadOrUnloadRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 32
    ba[5] = CheckSum(id, 3, 32)
    return ba;

def ServoLEDCtrlWrite(id, toggle):
    ba = bytearray(7)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 4
    ba[4] = 33
    ba[5] = toggle & 0x01
    ba[6] = CheckSum(id, 4, 33, toggle & 0x01)
    return ba;

def ServoLEDCtrlRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 34
    ba[5] = CheckSum(id, 3, 34)
    return ba;

def ServoLEDErrorWrite(id, fault):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 5
    ba[4] = 35
    ba[5] = fault
    ba[6] = CheckSum(id, 5, 35, fault)
    return ba;

def ServoLEDErrorRead(id):
    ba = bytearray(6)
    ba[0] = 0x55
    ba[1] = 0x55
    ba[2] = id & 0xff
    ba[3] = 3
    ba[4] = 36
    ba[5] = CheckSum(id, 3, 36)
    return ba;

def SendPacket(p):
    s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    s.write(p)
    s.close()

def test():
    s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)

    for a in range(0, 100000):
        for b in range(2, 4):
            angle = int(random.randrange(250, 750))
            print(f"Rotate motor {b} to { (angle / 1000.0 - 1.0) * 140 }")
            packet = ServoMoveTimeWrite(b, angle, 1000)
            s.write(packet)
        time.sleep(2.0)

    s.close()

def ResetAllMotors():
    s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    packet = ServoMoveTimeWrite(0xFE, 500, 1000)
    s.write(packet)
    s.close()


def IKRaise(C):
    C = 260 - C
    A = 130
    B = 130
    s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    elbowAngle = (math.acos((C*C -(A*A + B*B)) / (2 * A * B)) / math.pi * 180) / 140
    s.close()


#s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
#s.write(ServoPosRead(0x02))
#result = s.read_all()
#print(result)

#ResetAllMotors()

MotorAZero = 750
MotorBZero = 490

SendPacket(ServoMoveTimeWrite(0x2, MotorAZero, 1000))
SendPacket(ServoMoveTimeWrite(0x3, MotorBZero, 1000))

time.sleep(1.0)

for i in range(0, 10):
    C = 260 - i * 6
    A = 130
    B = 130
    elbowAngle = int((math.acos((C*C -(A*A + B*B)) / (2 * A * B)) / math.pi) * 642)

    rot = 0#i * 10
    print(f"{C}: { elbowAngle }\n")
    if elbowAngle < 500:
        SendPacket(ServoMoveTimeWrite(0x2, -rot + MotorAZero - elbowAngle, 10))
        SendPacket(ServoMoveTimeWrite(0x3, -rot + int(MotorBZero + elbowAngle / 2), 100))
        
    time.sleep(0.1)


time.sleep(1.0)


SendPacket(ServoMoveTimeWrite(0x2, MotorAZero, 300))
SendPacket(ServoMoveTimeWrite(0x3, MotorBZero, 300))