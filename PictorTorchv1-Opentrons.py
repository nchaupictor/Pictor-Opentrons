#Opentrons Pictor Torch Routine v1.0
#20/10/2017
#N CHAU

#--------------------------------------------------------------------------------------
#Import dependancies
#--------------------------------------------------------------------------------------
from opentrons import robot
from opentrons import containers, instruments
#--------------------------------------------------------------------------------------
#Initialise deck / pipettes
#--------------------------------------------------------------------------------------
#Set tiprack to be on the left edge so it can be adapted for low module use (or empty out space left of tip rack)
#TODO: Add JSON HTTP POST from main form to select the number of modules
tiprack200 = containers.load('tiprack-200ul','A2','tiprack')
plate = containers.load('96-flat','B1','plate')
trash = containers.load('point','D2')
trough = containers.load('trough-12row', slot)

p300 = instruments.Pipette(
    axis='b',
    max_volume = 300,
    channels = 8,
    aspirate_speed = 400, 
    dispense_speed = 600,
    trash_container = trash
    )

p50 = instruments.Pipette(
    axis='a',
    max_volume = 50,
    min_volume = 5,
    aspirate_speed = 400,
    dispense_speed = 600,
    trash_container = trash
    )

#--------------------------------------------------------------------------------------
#Functions 
#--------------------------------------------------------------------------------------
def wash(row):
    p300.pick_up_tip(tiprack(row))
    for i in range(3):
        p300.aspirate(100,trough(row))
        for j in range(2):
            p300.dispense(50,plate(j))
        p300.delay(seconds = 1)
        for j in range(2):
            p300.aspirate(75,plate(i))
        p300.dispense(toliquidwaste)
        p300.drop_tip()






#--------------------------------------------------------------------------------------
#Protocol Routine 
#--------------------------------------------------------------------------------------
#Step 0  -  Sample Dilution

p50.pick_up_tip(tiprack[96-i]) #Reserve tips in the back row for sample dilutions
#Step 1  -  Dispense Samples
for i in range(2):
    p300.pick_up_tip(tiprack[i])

    p300.return_tip()
#Step 2  -  Incubation
p300.delay(minutes = 30)
#Step 3  -  Aspirate Samples

#Step 4  -  Wash 1
#Step 5  -  Dispense Primary Antibody
p300.mix(3,50,trough['A1'])

#Step 6  -  Incubation
p300.delay(minutes = 30)
#Step 7  -  Aspirate Primary Antibody
p300.aspirate(75)

#Step 8  -  Wash 2 
wash(row)
#Step 9  -  Dispense Secondary Antibody
#Step 10 -  Incubation
#Step 11 -  Aspirate Secondary Antibody
#Step 12 -  Wash 3 
wash(row)
#Step 13 -  Dispense Detection Agent
#Step 14 -  Incubation
#Step 15 -  Aspirate Detection Agent
#Step 16 -  Wash 4
#Step 17 -  Drying Incubation 
