#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#Pictor Torch Routine
#This routine is for 32 Torch IgG and IgM samples only
#Version 1.0 | 11/12/2017
#PICTOR LIMITED 2017
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#Please prepare and layout the following items accordingly:
#--------------------------------------------------------------------------------------
#Deck Layout:
# A3- cooldeck      B3            C3-tiprack2   D3-             E3- tiprack3 
# A2                B2            C2-tuberack   D2-trash        E2- tiprack
# A1- serum         B1-sampleDil  C1-sample     D1-slide_deck   E1- 

#Tube Rack Layout:
#A1  [10mL Tube]: 5mL 10X Wash 
#A2  [10mL Tube]: 5mL 1X IgM Diluent 
#A3  [50mL Tube]: 15mL Water -> 18.52mL 1X Dil
#B1  [5mL Tube]:  2mL ConjG -> Temp store 1.852mL 10X Dil
#B2  [5mL Tube]:  2mL ConjM
#B3:
#B4  [50mL Tube]: 30mL Water -> 33mL 1X Wash
#C1  [5mL Tube]:  4mL Det
#C2  [5mL Tube]:  4mL Sub

#Cooldeck Layout:
# A5 - Substrate DAB  0.25mL  
# A4 - 4X IgM Diluent 1.5mL
# A3 - 20X Detection  0.25mL 
# A2 - 20X ConjM      0.1mL
# A1 - 20X ConjG      0.1mL    

#Tip Usage 
#21 p1000 single channel tips
#96 p50 multi channel tips       

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#Import dependencies
#--------------------------------------------------------------------------------------
from opentrons import robot
from opentrons import containers, instruments

robot.head_speed(x=18000, y=18000, z=5500, a=1100, b=1100)
robot.arc_height = 5
#--------------------------------------------------------------------------------------
#Initialise deck / pipettes
#--------------------------------------------------------------------------------------
#plate2 = containers.create(
#    'slide_deck',
#    grid = (8,12),
#    depth = 1.5,
#    diameter = 7.2,
#    spacing = (9.05,9.15)
#)

tiprack = containers.load('tiprack-200ul','E2','tiprack')
tiprack2 = containers.load('tiprack-1000ul','C3','tiprack2')
tiprack3 = containers.load('tiprack-200ul','E3','tiprack3')
trash = containers.load('trash-box','D2','trash')
serum = containers.load('96-PCR-tall','A1','serum')
sampleDil = containers.load('96-PCR-tall','B1','sampleDil')
cooldeck = containers.load('tube-rack-2ml','A3','cooldeck')
sample = containers.load('96-PCR-tall','C1','sample')
tuberack2 = containers.load('tube-rack-15_50ml2','C2','tuberack2')
plate2 = containers.load('slide_deck2','D1','plate2')

p50 = instruments.Pipette(
    name='p50',
    axis='a',
    min_volume = 5,
    max_volume = 50, 
    channels = 8,
    aspirate_speed = 300, 
    dispense_speed = 600,
    trash_container = trash,
    tip_racks=[tiprack,tiprack3]
    )

p1000 = instruments.Pipette(
    name='p1000',
    axis='b',
    max_volume = 1000,
    min_volume = 100,
    aspirate_speed = 300,
    dispense_speed = 1000,
    trash_container = trash,
    tip_racks=[tiprack2]
    )

#Configure Tube Rack
tuberack2['A1'].properties['height'] = 100
tuberack2['A2'].properties['height'] = 100
tuberack2['A3'].properties['height'] = 120
tuberack2['A4'].properties['height'] = 120
tuberack2['B1'].properties['height'] = 60
tuberack2['B2'].properties['height'] = 60
tuberack2['B4'].properties['height'] = 60
tuberack2['C1'].properties['height'] = 60
tuberack2['C2'].properties['height'] = 60

#--------------------------------------------------------------------------------------
#PROTOCOL BEGINS HERE
#--------------------------------------------------------------------------------------
#Step 0 - Sample Dilution
p1000.pick_up_tip(tiprack2(95))
'''
p1000.transfer(800,
                tuberack2('B4'),
                tuberack2('A4')
                )
p1000.transfer(800,
                tuberack2('A3'),
                tuberack2('A1')
                )

'''
robot.comment('Step 0 - Sample Dilution')
robot.comment('Preparing 1X Wash...')

#Transfer 3mL 10X Wash into 30mL of RO Water = 33mL 1X Wash
p1000.pick_up_tip(tiprack2(95))
p1000.transfer(3000, 
            tuberack2('A1'),
            tuberack2('B4'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 1.667mL 10X Wash into 15mL of RO Water = 16.67mL 1X Wash
p1000.transfer(1667,
            tuberack2('A1'),
            tuberack2('A3'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 1.852mL 10X Dil into 16.67mL 1X Wash = 18.52 1X Dil
p1000.transfer(1852,
            tuberack2('B1'),
            tuberack2('A3'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 1.9mL of 1X Dil into ConjG and conjM tubes
p1000.transfer(1900,
            tuberack2('A3'),
            tuberack2(['B1','B2']),
            #mix_before=(2,1000),
            new_tip='never',
            trash=False
            )

#Transfer 3.8mL of 1X Dil into detection tube
p1000.transfer(3800,
            tuberack2('A3'),
            tuberack2('C1'),
            new_tip='never',
            trash=False
            )

#Transfer 3.75mL of 1X Dil to ConjM tube
p1000.transfer(3750,
            tuberack2('A3'),
            tuberack2('A2'),
            new_tip='never',
            trash=False
            )
p1000.drop_tip()

#Transfer 1.25mL of 4x IgM Dil into 3.75mL 1X Dil = 5mL 1X IgM Dil
p1000.pick_up_tip(tiprack2(94))
p1000.transfer(1250,
            cooldeck('A4'),
            tuberack2('A2'),
            mix_after=(2,1000)
            )

#Dispense IgG samples into even rows
p1000.pick_up_tip(tiprack2(93))
p1000.distribute(54,
                tuberack2('A3'),
                sampleDil.rows('1','3','5','7'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip = 'never')

p1000.distribute(95,
                tuberack2('A3'),
                sample.rows('1','3','5','7'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip ='never')
p1000.drop_tip()

#Dispense IgM samples into odd rows
p1000.pick_up_tip(tiprack2(92))
p1000.distribute(54, 
                tuberack2('A2'),
                sampleDil.rows('2','4','6','8'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip = 'never')

p1000.distribute(90,
                tuberack2('A2'),
                sample.rows('2','4','6','8'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip ='never')
p1000.drop_tip()


count = 0
#Aspirate serum into first Dilution
for i in range(0,8,2):
    p50.pick_up_tip()
    p50.transfer(6,
                serum.rows(count),
                sampleDil.rows(i),
                blow_out = True,
                mix_after = (1,40),
                new_tip ='never'
                )
    count += count
#Second dilution 
    p50.transfer(5,
                sampleDil.rows(i),
                sample.rows(i),
                mix_after = (1,40),
                blow_out = True,
                trash=False)
count = 0
for i in range(1,9,2):
    p50.pick_up_tip()
    p50.transfer(6,
                serum.rows(count),
                #serum.rows(i),
                sampleDil.rows(i),
                blow_out = True,
                mix_after = (1,40),
                new_tip ='never'
                )
    count += count 
#Second dilution 
    p50.transfer(10,
                sampleDil.rows(i),
                sample.rows(i),
                mix_after = (1,40),
                blow_out = True,
                trash=False)

#--------------------------------------------------------------------------------------
#Step 1 - Dispense Samples
robot.comment('Step 1 - Dispense Samples')
p50.start_at_tip(tiprack.rows('1'))
p50.distribute(50,
                sample.rows('1','3','5','7'),
                plate2.rows('1','3','5','7'),
                mix_before = (1,40),
                blow_out = True,
                new_tip = 'always',
                trash = False)

p50.distribute(50,
                sample.rows('2','4','6','8'),
                plate2.rows('2','4','6','8'),
                mix_before = (1,40),
                blow_out = True,
                new_tip = 'always',
                trash = False)


#--------------------------------------------------------------------------------------
#Step 1.5 - Prepare Conjugate 
robot.comment('Step 1.5 - Preparing Conjugate')

#20-fold dilution for IgG 
p1000.pick_up_tip(tiprack2(91))
p1000.transfer(100,
                cooldeck('A1'),
                tuberack2('B1'),
                #trash=False,
                blow_out=True)
                #new_tip='never')

#20-fold dilution for IgM
p1000.pick_up_tip(tiprack2(90))
p1000.transfer(100,
                cooldeck('A2'),
                tuberack2('B2'),
                blow_out=True)

#--------------------------------------------------------------------------------------
#Step 2 - Incubation
#robot.comment('Step 2 - Incubation')
#p1000.delay(minutes = 27) #30

#--------------------------------------------------------------------------------------
#Step 3 - Aspirate Samples
robot.comment('Step 3 - Aspirate Samples')

p50.start_at_tip(tiprack.rows('1'))
p50.distribute(50, 
                plate2.rows('1','3','5','7'),
                trash,
                new_tip = 'always')

p50.distribute(50, 
                plate2.rows('2','4','6','8'),
                trash,
                new_tip = 'always')

#--------------------------------------------------------------------------------------
#Step 4 - Wash 1
robot.comment('Step 4 - Wash 1')

p1000.pick_up_tip(tiprack2(89))
p1000.distribute(50,
                tuberack2('B4'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                #trash = False,
                disposal_vol = 5)
p1000.drop_tip()

p50.pick_up_tip()
p50.distribute(50,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'always')


for i in range(2):
    p1000.pick_up_tip(tiprack2(88-i))
    p1000.distribute(50,
                tuberack2('B4'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                disposal_vol = 5)

    p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
    p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 5 - Dispense Primary Antibody (IgG / IgM)
robot.comment('Step 5 - Dispense Primary Antibody')
p1000.pick_up_tip(tiprack2(86))
p1000.distribute(50,
                tuberack2('B1'),
                plate2.rows('1','3','5','7'),
                new_tip = 'never',
                mix_before = (2,1000),
                disposal_vol = 5,
                trash = False)
p1000.return_tip()

p1000.pick_up_tip(tiprack2(85))
p1000.distribute(50,
                tuberack2('B2'),
                plate2.rows('2','4','6','8'),
                new_tip = 'never',
                mix_before = (2,1000),
                disposal_vol = 5,
                trash = False)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 5.5 - Prepare Detection dilution
robot.comment('Step 5.5 - Preparing Detection')
#20-fold dilution for detection 
p1000.pick_up_tip(tiprack2(84))
p1000.transfer(200,
                cooldeck('A3'),
                tuberack2['C1'],
                trash=False,
                blow_out=True)
                #new_tip='never')
#p1000.return_tip()

#--------------------------------------------------------------------------------------             
#Step 6 - Incubation 
robot.comment('Step 6 - Incubation')
#p1000.delay(minutes = 29) 
#robot.home()

#--------------------------------------------------------------------------------------
#Step 7 - Aspirate Primary Antibody (Add in IgG / IgM split)
robot.comment('Step 7 - Aspirate Primary Antibody')

p1000.pick_up_tip(tiprack2(86))
p1000.consolidate(62.5,
                plate2.rows('1','3','5','7'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

p1000.pick_up_tip(tiprack2(85))
p1000.consolidate(62.5,
                plate2.rows('2','4','6','8'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 8 - Wash 2
robot.comment('Step 8 - Wash 2')
for i in range(3):
    p1000.pick_up_tip(tiprack2(83-i))
    p1000.distribute(50,
                tuberack2('B4'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                disposal_vol = 5)

    p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
    p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 9 - Dispense Detection
robot.comment('Step 9 - Dispense Detection')
p1000.pick_up_tip(tiprack2(84))
p1000.distribute(50,
                tuberack2('C1'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                mix_before = (2,1000),
                disposal_vol = 5,
                trash = False)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 10 - Incubation
#robot.home()
robot.comment('Step 10 - Incubation')
#p1000.delay(minutes = 28) 

#--------------------------------------------------------------------------------------
#Step 10.5 - Prepare Substrate
robot.comment('Step 9.5 - Preparing Substrate')
p1000.pick_up_tip(tiprack2(80))
p1000.transfer(200,
                cooldeck('A5'),
                tuberack2('C2'),
                mix_before = (2,1000),
                new_tip='never',
                blow_out = True)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 11 - Aspirate Detection
robot.comment('Step 11 - Aspirate Detection')
p1000.pick_up_tip(tiprack2(84))
p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 12 - Wash 3
robot.comment('Step 12 - Wash 3')
for i in range(3):
    p1000.pick_up_tip(tiprack2(79-i))
    p1000.distribute(50,
                tuberack2('B4'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                disposal_vol = 5)

    p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
    p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 13 - Dispense Substrate DAB
robot.comment('Step 13 - Dispense Substrate')
p1000.pick_up_tip(tiprack2(80))
p1000.distribute(50,
                tuberack2('C2'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                mix_before = (2,1000),
                disposal_vol = 5,
                trash = False)

#--------------------------------------------------------------------------------------
#Step 14 - Incubation
robot.comment('Step 14 - Incubation')
#p1000.delay(minutes = 5) 

#--------------------------------------------------------------------------------------
#Step 15 - Aspirate Substrate
robot.comment('Step 15 - Aspirate Substrate')
for i in range(2):
    p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 16 - Wash 4
robot.comment('Step 16 - Wash 4')
p1000.pick_up_tip(tiprack2(76))
p1000.distribute(50,
                tuberack2('B4'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                disposal_vol = 5)

p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 17 - Drying Incubation
robot.comment('Step 17 - Drying Incubation')
#p1000.delay(minutes = 30) 

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#ASSAY COMPLETE
robot.comment('Assay Complete!')
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
