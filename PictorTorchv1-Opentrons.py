#Opentrons Pictor Torch Routine v1.0
#20/10/2017
#N CHAU

#Layout:
# A3 tube rack (B3) waste (C3) D3 E 3 
# A2 sample (B2)  liquidwaste (C2) D2 E2 
# A1 tiprack (B1) trough (C1) slide_deck (D1) E1
#--------------------------------------------------------------------------------------
#Import dependancies
#--------------------------------------------------------------------------------------
from opentrons import robot
from opentrons import container, instruments
#--------------------------------------------------------------------------------------
#Initialise deck / pipettes
#--------------------------------------------------------------------------------------
#Set tiprack to be on the left edge so it can be adapted for low module use (or empty out space left of tip rack)
#TODO: Add JSON HTTP POST from main form to select the number of modules
tiprack200 = container.load('tiprack-200ul','A2','tiprack')
#plate = container.load('96-flat','B1','plate')
plate = container.create(
    'slide_deck',
    grid = (8,12),
    depth = 1.5,
    diameter = 7.2,
    spacing = (9,9)#skip any tipCount % 3 == 0 rows 
)
plate = container.load(slide_deck,'B1')
sample = container.load('96-PCR-tall', slot)
trash = container.load('point','D2')
fluidtrash = container.load('point','C2')
trough = container.load('trough-12row', slot)

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
#Helper Functions 
#--------------------------------------------------------------------------------------
#Generic washing function
def wash(row):
    p300.pick_up_tip(tiprack200(row))
    for i in range(3):
        p300.aspirate(100,trough(row))
        for j in range(2):
            p300.dispense(50,plate(j))
        p300.delay(seconds = 1)
        for j in range(2):
            p300.aspirate(75,plate(i))
        p300.dispense(fluidtrash)
        p300.drop_tip()

#Merge string together with tip counter variable
def merge(num):
    return 'A' + str(num)

#Generic aspiration function 
def aspirate(row):
    p300.pick_up_tip(tiprack200(row))
    for i in range(2):
        p300.aspirate(75,plate(i))
    p300.dispense(fluidtrash)
    p300.drop_tip()
    
#TODO: Use distribute function 
#--------------------------------------------------------------------------------------
#Protocol Routine 
#--------------------------------------------------------------------------------------
tipCount  = 2
#Step 0  -  Sample Dilution
robot.comment('Step 0 - Sample Dilution')
#TODO: Finalise tube racks for sample dilution steps 
#TODO: Iterate tipCount
p50.pick_up_tip(tiprack[96-i]) #Reserve tips in the back row for sample dilutions









#Step 1  -  Dispense Samples
robot.comment('Step 1 - Dispense Samples')
for i in range(2):
    p300.pick_up_tip(tiprack200(i))
    p300.aspirate(50,sample(i))
    p300.dispense(50,plate(i))
    p300.return_tip()

#Step 2  -  Incubation
robot.comment('Step 2 - Incubation')
p300.delay(minutes = 30)

#Step 3  -  Aspirate Samples
robot.comment('Step 3 - Aspirate Samples')
for i in range(2):
    p300.pick_up_tip(tiprack200(i))
    p300.aspirate(75,plate(i))
    p300.dispense(fluidtrash)
    p300.drop_tip()

#Step 4  -  Wash 1
robot.comment('Step 4 - Wash 1 ')
p300.pick_up_tip(tiprack200(tipCount))
p300.aspirate(100,trough[merge(tipCount)])
for i in range(2):
    p300.dispense(50,plate(i))

p300.aspirate(75,plate(0))
p300.dispense(fluidwaste)
p300.drop_tip()

p300.pick_up_tip(tiprack200(tipCount))
p300.aspirate(75,plate(1))
p300.dispense(fluidtrash)
p300.drop_tip()

#Step 5  -  Dispense Primary Antibody
robot.comment('Step 5 - Dispense Primary Antibody')
p300.pick_up_tip(tiprack200(tipCount))
p300.mix(3,50,trough[merge(tipCount)])
p300.aspirate(100)
for i in range(2):
    p300.dispense(50,plate(i))

#Step 6  -  Incubation
robot.comment('Step 6 - Incubation')
p300.delay(minutes = 30)

#Step 7  -  Aspirate Primary Antibody
robot.comment('Step 7 - Aspirate Primary Antibody')
aspirate(tipCount)

#Step 8  -  Wash 2 
robot.comment('Step 8 - Wash 2')
wash(row)

#Step 9  -  Dispense Secondary Antibody
robot.comment('Step 9 - Dispense Secondary Antibody')
p300.mix(3,50,trough[merge(tipCount)])
p300.aspirate(100)
for i in range(2):
    p300.dispense(50,plate(i))

#Step 10 -  Incubation
robot.comment('Step 10 - Incubation')
p300.delay(minutes = 30)

#Step 11 -  Aspirate Secondary Antibody
robot.comment('Step 11 - Aspirate Secondary Antibody')
aspirate(tipCount)

#Step 12 -  Wash 3 
robot.comment('Step 12- Wash 3')
wash(row)

#Step 13 -  Dispense Detection Agent
robot.comment('Step 13 - Dispense Detection Agent')
p300.mix(3,50,trough[merge(tipCount)])
p300.aspirate(100)
for i in range(2):
    p300.dispense(50,plate(i))

#Step 14 -  Incubation
robot.comment('Step 14 - Incubation')
p300.delay(minutes = 5)

#Step 15 -  Aspirate Detection Agent
robot.comment('Step 15 - Aspirate Detection Agent')
aspirate(tipCount)

#Step 16 -  Wash 4
robot.comment('Step 16 - Wash 4')
p300.pick_up_tip(tiprack200(row))
p300.aspirate(100,trough(row))
    for i in range(2):
        p300.dispense(50,plate(i))
    p300.delay(seconds = 1)
    for i in range(2):
        p300.aspirate(75,plate(i))
    p300.dispense(fluidtrash)
    p300.drop_tip()

#Step 17 -  Drying Incubation 
robot.comment('Step 17 - Drying Incubation')
p300.delay(minutes = 30)
