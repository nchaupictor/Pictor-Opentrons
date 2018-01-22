#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#Pictor ENA Routine
#This routine is for 64 ENA samples only
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
#A2  [10mL Tube]: 7mL Water -> 7.78mL 1X Wash  -> 8.64mL 1X Dil
#A3  [50mL Tube]: 8mL Water -> 8.9mL 1X Wash -> 9.9mL 0.1X Dil
#B1  [5mL Tube]:  1mL 10X Dil
#B2  [5mL Tube]:  4mL ConjG
#B3: 
#B4  [50mL Tube]: 30mL Water -> 33mL 1X Wash
#C1  [5mL Tube]:  4mL Det
#C2  [5mL Tube]:  4mL Sub

#Cooldeck Layout:
# A5 - Substrate DAB  0.25mL
# A4 - Empty
# A3 - 20X Detection  0.25mL 
# A2 - Empty 
# A1 - 20X ConjG      0.25mL

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

#Transfer 0.78mL 10X Wash into 7mL RO Water = 7.78mL 1X Wash
p1000.transfer(780,
            tuberack2('A1'),
            tuberack2('A2'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 0.89mL 10X Wash into 8mL RO Water = 8.9mL 1X Wash
p1000.transfer(3000, 
            tuberack2('A1'),
            tuberack2('A3'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )


#Transfer 0.86mL 10X Dil into 7.78mL 1X Wash = 8.64mL 1X Dil
p1000.transfer(860,
            tuberack2('B1'),
            tuberack2('A2'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 0.98mL 1X Dil into 8.9mL 1X Wash = 9.9mL 0.1X Dil
p1000.transfer(980,
            tuberack2('A2'),
            tuberack2('A3'),
            mix_after=(1,1000),
            new_tip='never',
            trash=False
            )

#Transfer 3.8mL of 1X Dil into ConjG and Det tubes
p1000.transfer(3800,
            tuberack2('A2'),
            tuberack2(['B2','C1']),
            new_tip='never',
            trash=False
            )


p1000.pick_up_tip(tiprack2(94))
robot.comment('Preparing Sample Dilutions...')
#Fill first dilution plate with 54uL and second dilution plate with 95uL of 0.1X Dil
p1000.distribute(54,
                tuberack2('A3'),
                sampleDil.rows('1', to= '8'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip = 'never')

p1000.distribute(90,
                tuberack2('A3'),
                sample.rows('1', to= '8'),
                disposal_vol = 5,
                blow_out = True,
                trash=False,
                new_tip ='never')
p1000.drop_tip()

#Aspirate serum into first Dilution
for i in range(8):
    p50.pick_up_tip()
    p50.transfer(6,
                serum.rows(i),
                sampleDil.rows(i),
                blow_out = True,
                mix_after = (1,40),
                new_tip ='never'
                )
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
                sample.rows('1', to= '8'),
                plate2.rows('1', to= '8'),
                mix_before = (1,40),
                blow_out = True,
                new_tip = 'always',
                trash = False)

#--------------------------------------------------------------------------------------
#Step 1.5 - Prepare Conjugate
robot.comment('Step 1.5 - Preparing Conjugate')
p1000.pick_up_tip(tiprack2(93))
p1000.transfer(200,
            cooldeck('A1'),
            tuberack2('B2'),
            blow_out=True)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 2 - Incubation
#robot.comment('Step 2 - Incubation')
#p50.delay(minutes = 29) #30

#--------------------------------------------------------------------------------------
#Step 3 - Aspirate Samples
robot.comment('Step 3 - Aspirate Samples')

p50.start_at_tip(tiprack.rows('1'))
p50.distribute(50, 
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'always')

#--------------------------------------------------------------------------------------
#Step 4 - Wash 1
robot.comment('Step 4 - Wash 1')

p1000.pick_up_tip(tiprack2(92))
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
    p1000.pick_up_tip(tiprack2(91-i))
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
#Step 5 - Dispense Primary Antibody (IgG)
robot.comment('Step 5 - Dispense Primary Antibody')
p1000.pick_up_tip(tiprack2(88))
p1000.distribute(50,
                tuberack2('A1'),
                plate2.rows('1', to= '8'),
                new_tip = 'never',
                mix_before = (2,1000),
                disposal_vol = 5,
                trash = False)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 5.5 - Preparing Detection
robot.comment('Step 5.5 - Preparing Detection')
p1000.pick_up_tip(tiprack2(87))
p1000.transfer(200,
                cooldeck('A3'),
                tuberack2('C1'),
                trash=False,
                blow_out=True)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 6 - Incubation 
robot.comment('Step 6 - Incubation')
#p1000.delay(minutes = 30) 
#robot.home()

#--------------------------------------------------------------------------------------
#Step 7 - Aspirate Primary Antibody 
robot.comment('Step 7 - Aspirate Primary Antibody')

p1000.pick_up_tip(tiprack2(88))
p1000.consolidate(62.5,
                plate2.rows('1', to= '8'),
                trash,
                new_tip = 'never',
                blow_out = True)
p1000.drop_tip()

#--------------------------------------------------------------------------------------
#Step 8 - Wash 2
robot.comment('Step 8 - Wash 2')
for i in range(3):
    p1000.pick_up_tip(tiprack2(86-i))
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
p1000.pick_up_tip(tiprack2(87))
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
robot.home()
robot.comment('Step 10 - Incubation')
#p1000.delay(minutes = 28) 

#--------------------------------------------------------------------------------------
#Step 10.5 - Prepare Substrate
robot.comment('Step 9.5 - Preparing Substrate')
p1000.pick_up_tip(tiprack2(83))
p1000.transfer(250,
                cooldeck('A5'),
                tuberack2('C2'),
                mix_before = (2,1000),
                new_tip='never',
                blow_out = True)
p1000.return_tip()

#--------------------------------------------------------------------------------------
#Step 11 - Aspirate Detection
robot.comment('Step 11 - Aspirate Detection')
p1000.pick_up_tip(tiprack2(87))
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
    p1000.pick_up_tip(tiprack2(82-i))
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
p1000.pick_up_tip(tiprack2(83))
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
p1000.pick_up_tip(tiprack2(79))
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