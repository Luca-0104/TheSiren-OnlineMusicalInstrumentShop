"""
pm_lst_example = [
    # product 1 ----------------------------------------------------
    [
        "product-name-test",        # product name
        1,                          # brand id
        1,                          # cate id - C
        7,                          # cate id - T
        53,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',          # model name
                'model-description-test',   # m description
                100,                        # m price
                2,                          # kg
                [
                    'p1m1-1.png',
                    'p1m1-2.png',
                    'p1m1-3.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 1 ----------------------------------------------------
    # []
]


Category:
    C: id 1-6
    T: id 7-52
    A: id 53-56
"""

pm_lst = [
    # product 1 ----------------------------------------------------
    [
        "Stentor Amati model violin",  # product name
        4,  # Stentor
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Stentor Amati model violin',  # model name
                'A beautiful violin modelled on an original violin of 1694 by Nicola Amati. It is made fom selected and figured European tonewoods and is finished with a hand applied traditional varnish which brings out the appearance of the wood. This superb handcrafted instrument features the deeper arching of Amati style. It is finished in a warm golden base colour with traditional hand applied shellac varnish. It has Pirastro strings and is individually workshop fitted.',
                # m description
                12490,  # m price
                1.5,  # kg
                [
                    'g-p1m1-1.jpg',
                    'g-p1m1-2.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 2 ----------------------------------------------------
    [
        "Stentor Arcadia viola",  # product name
        4,  # Stentor
        1,  # cate id - C
        8,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Stentor Arcadia viola',  # model name
                "The Stentor Arcadia is the top of Stentor's range of high grade orchestral models. These are superb handcrafted instruments, carved from the most select, highly figured tonewoods. The Stentor Arcadia viola is made in a specialist hand workshop within the Stentor factory, where the most skilled individual workers produce under the close supervision of a master maker, in a traditional luthier's environment that would be familiar to makers throughout the centuries. The superior sound is unique to each instrument and reflects the individuality of each one. The viola is finished with a hand-applied traditional shellac varnish and fitted with Pirastro strings. All instruments are individually workshop fitted.",
                # m description
                23100,  # m price
                2,  # kg
                [
                    'g-p2m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],
    # product 3 ----------------------------------------------------
    [
        "Stentor Arcadia cello",  # product name
        4,  # Stentor
        1,  # cate id - C
        9,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Stentor Arcadia cello',  # model name
                'The Stentor Arcadia is the top of Stentor’s range of high-grade orchestral models. These are superb handcrafted instruments, carved from the most select, highly figured tonewoods. The Stentor Arcadia cello is made in a specialist hand workshop within the Stentor factory. This individual cello is finished with a hand-applied traditional shellac varnish and fitted with professional quality branded strings. All instruments are individually workshop fitted.',
                # m description
                33600,  # m price
                7.5,  # kg
                [
                    'g-p3m1-1.jpg',
                    'g-p3m1-2.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],
    # product 4 ----------------------------------------------------
    [
        "Stentor Arcadia double bass",  # product name
        4,  # Stentor
        1,  # cate id - C
        10,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Stentor Arcadia double bass',  # model name
                "The Stentor Arcadia double bass is an excellent handcrafted instrument, hand carved from selected solid tonewoods, with inlaid purfling. It features a fully carved well flamed back and front and is finished with a hand applied traditional shellac varnish. Each instrument is individually workshop fitted. The Stentor Arcadia is the top of Stentor's range of high-grade orchestral models. These are superb handcrafted instruments, carved from selected and figured tonewoods. It is made in a specialist bass workshop within the Stentor factory, in a traditional luthier's environment that would be familiar to makers throughout the centuries. This produces fine instruments with a superior finish and sound that reflects the making of each instrument.",
                # m description
                35900,  # m price
                5.5,  # kg
                [
                    'g-p4m1-1.jpg',
                    'g-p4m1-2.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 5 ----------------------------------------------------
    [
        "Lowden 50 Series Guitar",  # product name
        1,  # brand id
        1,  # cate id - C
        11,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Lowden 50 Series Guitar Indian Rosewood',  # model name
                'The 50 series can be described as the Lowden Custom Shop. With the 50 Series, customers have the opportunity to choose any combination of woods in any body size as well as having the choice of tone woods not available in the 35 Series such as African Blackwood and Brazilian Rosewood. Moreover, the woods that are used are Master Grade tone woods; the best of the best tone woods available anywhere chosen for their exceptional tonal and visual properties.',
                # m description
                3900,  # m price
                3.5,  # kg
                [
                    'g-p5m1-1.png',
                    'g-p5m1-2.jpg',
                    'g-p5m1-3.jpg',
                    'g-p5m1-4.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'Lowden 50 Series Guitar Walnut',  # model name
                'The 50 series can be described as the Lowden Custom Shop. With the 50 Series, customers have the opportunity to choose any combination of woods in any body size as well as having the choice of tone woods not available in the 35 Series such as African Blackwood and Brazilian Rosewood. Moreover, the woods that are used are Master Grade tone woods; the best of the best tone woods available anywhere chosen for their exceptional tonal and visual properties.',
                # m description
                4200,  # m price
                3.5,  # kg
                [
                    'g-p5m2-1.png',
                    'g-p5m2-2.jpg',
                    'g-p5m2-3.jpg'
                ]
            ],
            # model 3 ----------------------------------------------------------
            [
                'Lowden 50 Series Guitar Honduras Rosewood',  # model name
                'The 50 series can be described as the Lowden Custom Shop. With the 50 Series, customers have the opportunity to choose any combination of woods in any body size as well as having the choice of tone woods not available in the 35 Series such as African Blackwood and Brazilian Rosewood. Moreover, the woods that are used are Master Grade tone woods; the best of the best tone woods available anywhere chosen for their exceptional tonal and visual properties.',
                # m description
                4600,  # m price
                3.7,  # kg
                [
                    'g-p5m3-1.png',
                    'g-p5m3-2.jpg'
                ]
            ]
        ]
    ],

    # product 6 ----------------------------------------------------
    [
        "Gibson Les Paul Standard '50s",  # product name
        2,  # brand id
        1,  # cate id - C
        11,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                "Gibson Les Paul Standard '50s Gold Top",  # model name
                "A Classic, Reborn The new Les Paul Standard returns to the classic design that made it relevant, played and loved -- shaping sound across generations and genres of music. It pays tribute to Gibson's Golden Era of innovation and brings authenticity back to life. The Les Paul Standard 50's has a solid mahogany body with a maple top, a rounded 50's-style mahogany neck with a rosewood fingerboard and trapezoid inlays. It's equipped with an ABR-1, the classic-style Tune-O-Matic bridge, aluminum stop bar tailpiece, vintage deluxe tuners with keystone buttons, and aged gold tophat knobs. The calibrated Burstbucker 1 (neck) and Burstbucker 2 (bridge) pickups are loaded with AlNiCo II magnets, audio taper potentiometers and orange drop capacitors.",
                # m description
                2699,  # m price
                3.5,  # kg
                [
                    'g-p6m1-1.png',
                    'g-p6m1-2.png',
                    'g-p6m1-3.png',
                    'g-p6m1-4.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                "Gibson Les Paul Standard '50s Heritage Cherry Sunburst",  # model name
                "A Classic, Reborn The new Les Paul Standard returns to the classic design that made it relevant, played and loved -- shaping sound across generations and genres of music. It pays tribute to Gibson's Golden Era of innovation and brings authenticity back to life. The Les Paul Standard 50's has a solid mahogany body with a maple top, a rounded 50's-style mahogany neck with a rosewood fingerboard and trapezoid inlays. It's equipped with an ABR-1, the classic-style Tune-O-Matic bridge, aluminum stop bar tailpiece, vintage deluxe tuners with keystone buttons, and aged gold tophat knobs. The calibrated Burstbucker 1 (neck) and Burstbucker 2 (bridge) pickups are loaded with AlNiCo II magnets, audio taper potentiometers and orange drop capacitors.",
                # m description
                2699,  # m price
                3.5,  # kg
                [
                    'g-p6m2-1.png',
                    'g-p6m2-2.png',
                    'g-p6m2-3.png',
                    'g-p6m2-4.png'
                ]
            ],
            # model 3 ----------------------------------------------------------
            [
                "Gibson Les Paul Standard '50s Tobacco Burst",  # model name
                "A Classic, Reborn The new Les Paul Standard returns to the classic design that made it relevant, played and loved -- shaping sound across generations and genres of music. It pays tribute to Gibson's Golden Era of innovation and brings authenticity back to life. The Les Paul Standard 50's has a solid mahogany body with a maple top, a rounded 50's-style mahogany neck with a rosewood fingerboard and trapezoid inlays. It's equipped with an ABR-1, the classic-style Tune-O-Matic bridge, aluminum stop bar tailpiece, vintage deluxe tuners with keystone buttons, and aged gold tophat knobs. The calibrated Burstbucker 1 (neck) and Burstbucker 2 (bridge) pickups are loaded with AlNiCo II magnets, audio taper potentiometers and orange drop capacitors.",
                # m description
                2699,  # m price
                3.5,  # kg
                [
                    'g-p6m3-1.png',
                    'g-p6m3-2.png',
                    'g-p6m3-3.png',
                    'g-p6m3-4.png'
                ]
            ]
        ]
    ],

    # product 7 ----------------------------------------------------
    [
        "Gibson B.B. King Lucille Legacy - Transparent Ebony",  # product name
        2,  # brand id
        1,  # cate id - C
        11,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Gibson B.B. King Lucille Legacy - Transparent Ebony',  # model name
                "A Tribute to the King The legendary Gibson B.B. King Lucille Legacy returns to the Custom Shop ES™ lineup as a core Artist model. Lucille features all of the high-end appointments that are fit for a King. Highlights include gold hardware, including a gold “B.B. King” engraved truss rod cover and a TP-6 tailpiece with fine tuners. A “Lucille” mother of pearl inlay adorns the headstock, and the ebony fretboard features split block mother of pearl inlays. A mono Varitone switch, along with four audio taper CTS® potentiometers and paper-in-oil Bumblebee capacitors, are paired to Gibson Custombucker humbucking pickups. The legendary semi-hollowbody design remains, but the f-holes are gone, in keeping with B.B. King’s personal preferences. The top, back, and sides of the body feature stunning figured maple veneer, which is visible through the Transparent Ebony nitrocellulose lacquer finish, making Lucille a very special guitar that’s fit for blues royalty.",
                # m description
                6999,  # m price
                4.5,  # kg
                [
                    'g-p7m1-1.png',
                    'g-p7m1-2.png',
                    'g-p7m1-3.png',
                    'g-p7m1-4.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 8 ----------------------------------------------------
    [
        "Gibson Thunderbird Bass",  # product name
        2,  # brand id
        1,  # cate id - C
        12,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Gibson Thunderbird Bass Tobacco Burst',  # model name
                "Hard Rock Low End The Gibson Thunderbird has the classic reverse body and headstock design as originally introduced in 1963 as Gibson's first neck-through-body bass design. The traditional 9-ply mahogany/walnut neck through body construction provides a thundering low end response and a piano like sustain. The narrow nut width and rounded neck profile neck feels both fast and intuitive. The Thunderbird high output, ceramic magnet loaded humbucking pickups (neck and bridge) deliver the sonic and iconic low end voice for which the Thunderbird is known. This model type is in the color of Tobacco Burst",
                # m description
                2299,  # m price
                3.2,  # kg
                [
                    'g-p8m1-1.png',
                    'g-p8m1-2.png',
                    'g-p8m1-3.png',
                    'g-p8m1-4.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'Gibson Thunderbird Bass Ebony',  # model name
                "Hard Rock Low End The Gibson Thunderbird has the classic reverse body and headstock design as originally introduced in 1963 as Gibson's first neck-through-body bass design. The traditional 9-ply mahogany/walnut neck through body construction provides a thundering low end response and a piano like sustain. The narrow nut width and rounded neck profile neck feels both fast and intuitive. The Thunderbird high output, ceramic magnet loaded humbucking pickups (neck and bridge) deliver the sonic and iconic low end voice for which the Thunderbird is known. This model type is in the color of Ebony",
                # m description
                2299,  # m price
                3.2,  # kg
                [
                    'g-p8m2-1.png',
                    'g-p8m2-2.png',
                    'g-p8m2-3.png',
                    'g-p8m2-4.png'
                ]
            ]
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 9 ----------------------------------------------------
    [
        "Martin D-45S AUTHENTIC 1936 Guitar",  # product name
        5,  # brand id
        1,  # cate id - C
        11,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Martin D-45S AUTHENTIC 1936 Guitar',  # model name
                "Here to remind you why you fell in love with us in the first place, the new Authentics are constructed the old way - with hide glue, throughout, and historically-accurate detailing confirmed by using a CAT scan machine located at the Smithsonian Institution. The D-45S Authentic 1936 is based on a large body D-45 located in our museum, and features Brazilian rosewood back and sides, an Adirondack spruce top, period-correct '45' Authentic style appointments, and includes gold tuners with hand-engraved butterbean knobs. Martin’s new VINTAGE TONE SYSTEM® (VTS) is employed for the top and braces. The new Martin VINTAGE TONE SYSTEM® (VTS) uses a unique recipe that is based on the historic torrefaction system. The VTS acts much like a time machine in which Martin can target certain time periods and age the top/braces to that era. This focused method allows Martin’s craftsmen and women to recreate not only the pleasing visual aesthetics of a vintage guitar, but also reproduce the special tones previously reserved for vintage instruments.",
                # m description
                49999,  # m price
                2.2,  # kg
                [
                    'g-p9m1-1.jpg',
                    'g-p9m1-4.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'Martin D-45S AUTHENTIC 1936 Aged Guitar',  # model name
                "The D-45S Authentic 1936 Aged is based on an extremely rare large body D-45 that was once displayed in the Martin museum. It features Brazilian rosewood back and sides, a pre-aged Adirondack spruce top, and period-correct Style 45 appointments, including gold tuners with hand-engraved butterbean knobs. A newly constructed masterpiece that looks and sounds like it’s been played for 80 years, the D-45S Authentic 1936 Aged includes all of the goodness instilled within Martin’s Authentic Series, like hide glue construction and hand-scalloped X-bracing. It also boasts the VINTAGE TONE SYSTEM® (VTS) that ages the wood to replicate the sound of a highly sought-after vintage Martin, both in tone and appearance.",
                # m description
                51999,  # m price
                2.3,  # kg
                [
                    'g-p9m2-1.jpg'
                ]
            ]
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 10 ----------------------------------------------------
    [
        "Martin T1 UKE",  # product name
        5,  # brand id
        1,  # cate id - C
        13,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Martin T1K UKE',  # model name
                "Martin has built the world’s finest ukuleles since 1916, and tenor ukes since 1929 that have long been prized for their full-bodied voice and great volume. The T1K tenor-sized model features top, back and sides crafted of solid Hawaiian koa, a wood native to Hawaii and a favorite of island players. The entire body is finished in high quality satin lacquer, and features an applied dovetail neck joint. The T1K Uke is a beautiful example of why Martin is still the name in superior quality ukuleles.",
                # m description
                499,  # m price
                1.4,  # kg
                [
                    'g-p10m1-1.jpg',
                    'g-p10m1-2.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'Martin T1 UKE STREETMASTER',  # model name
                "We’ve been making tenor-sized ukuleles since 1929, but nothing quite like this. An ultra-thin finish creates a beautifully weathered appearance that feels as if it’s an old friend you’ve been playing for years. The top, back and sides are all mahogany, making it lightweight with a bright tone. If you play guitar and want to learn the uke, this size makes for a comfortable transition, and it's great for both a child and full-grown adult. The T1 StreetMaster® brings together premier sound, outstanding playability, and easy affordability in one gorgeous instrument.",
                # m description
                449,  # m price
                1.3,  # kg
                [
                    'g-p10m2-1.jpg',
                    'g-p10m2-2.jpg',
                    'g-p10m2-3.jpg'
                ]
            ],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 11 ----------------------------------------------------
    [
        "Yamaha TRBX305 Bass",  # product name
        16,  # brand id
        1,  # cate id - C
        12,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha TRBX305 Bass',  # model name
                '5 strings version of TRBX300 series Solid mahogany construction Maple / Mahogany 5-Piece Neck Slim 43mm nut width 2-band active EQ with 5-way Performance EQ preset switch',  # m description
                999,  # m price
                2,  # kg
                [
                    'g-p11m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 12 ----------------------------------------------------
    [
        "Lyon&Healy PREMIUM STYLE 26 GOLD Harp",  # product name
        17,  # brand id
        1,  # cate id - C
        14,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Lyon&Healy PREMIUM STYLE 26 GOLD Harp',  # model name
                'A stately harp designed by Lyon & Healy in the late 1800s, the Style 26 integrates nineteenth century Gothic revival styles with Renaissance detail. The harp is hand-gilded with 23+ karat gold leaf and burnished to feature the dimension of the relief and the hexagonal column. The hand-painted soundboard decoration using 23+ karat gold leaf features intricate brush strokes that climb up the length of the soundboard, interlaced with rose blooms.',  # m description
                158790,  # m price
                37,  # kg
                [
                    'g-p12m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 13 ----------------------------------------------------
    [
        "HuQiu Special selection of old mahogany professional Erhu",  # product name
        17,  # brand id
        1,  # cate id - C
        15,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'HuQiu Special selection of old mahogany professional Erhu',  # model name
                'Stage performance special erhu, a full set of accessories as gift',  # m description
                12800,  # m price
                1.2,  # kg
                [
                    'g-p13m1-1.jpg',

                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 14 ----------------------------------------------------
    [
        "HuQiu 21 string red Phoenix Guzheng",  # product name
        17,  # brand id
        1,  # cate id - C
        16,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'HuQiu 21 string red Phoenix Guzheng',  # model name
                'Beginner, performance, entertainment professional Guzheng, buy and get a full set of accessories for free',  # m description
                12600,  # m price
                4.5,  # kg
                [
                    'g-p14m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 15 ----------------------------------------------------
    [
        "Dunhuang Guqin (senior) (Aged broken grain wood)",  # product name
        17,  # brand id
        1,  # cate id - C
        17,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Dunhuang Guqin (senior) (Aged broken grain wood)',  # model name
                'Dunhuang Guqin (senior) (Aged broken grain wood)',  # m description
                15900,  # m price
                3.5,  # kg
                [
                    'g-p15m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 16 ----------------------------------------------------
    [
        "Huqiu White acid branch wax professional lute",  # product name
        17,  # brand id
        1,  # cate id - C
        18,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'White acid branch wax professional lute',  # model name
                'Pure sound quality, aesthetic appearance, boutique customization',  # m description
                44500,  # m price
                2.5,  # kg
                [
                    'g-p16m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 17 ----------------------------------------------------
    [
        "Yamaha 900/800 Series Handmade Flutes",  # product name
        16,  # brand id
        2,  # cate id - C
        19,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha 900/800 Series Handmade Flutes',  # model name
                'Inspired to start afresh, we went back to a clean slate applying all of the knowledge, advancements, and skills we’ve obtained over the last two decades crafting some of the finest handmade flutes available today into the design of an entirely new line of handmade instruments. Focusing on innovation, we’ve created some instruments that change the image of the handmade flute significantly. They offer tone with charm and depth, and a wide dynamic range that allows performers to play with a wide range of expression and the tone and volume flutists have long desired. Top-of-the-line handmade gold flutes offer a rich, deep tone with outstanding presence in orchestral settings. Highly responsive with a wide dynamic range that spans from rich, sensitive pianissimo to highly resonant fortissimo they allow the flautist to discover new limits of musical expression. From the finest details to their overall design, every part, process, and component on these handmade silver flutes is designed to function in harmony with the rest.',  # m description
                35900,  # m price
                1.3,  # kg
                [
                    'g-p17m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 18 ----------------------------------------------------
    [
        "Yamaha YCL-CSVR-ASP/CSVRA-ASP Clarinet",  # product name
        16,  # brand id
        2,  # cate id - C
        20,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha YCL-CSVR-ASP/CSVRA-ASP Clarinet',  # model name
                'The Custom CSVR clarinets were specifically designed with the input of professional clarinet educators. This led to a complete revitalization of Yamaha clarinets seen with the SEVR, CSGIII, and now the CSVR-ASP clarinets. The Atelier Special clarinet gives players an exacting level of consistency and quality for the most nuance control and performance, with a darker and more projecting tone than that of the original CSVR.',  # m description
                15800,  # m price
                1.2,  # kg
                [
                    'g-p18m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 19 ----------------------------------------------------
    [
        "Yamaha YOB-841L Oboe",  # product name
        16,  # brand id
        2,  # cate id - C
        21,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha YOB-841L Oboe',  # model name
                "Yamaha oboes achieve a clear sound quality and superb intonation by dramatically improving the precision and stability of the bore. Also to cope with various durability issues inherent in wooden wind instruments, Duet+ models employ innovative techniques to form a protective layer next to the air column. The combination of precious wood and state-of -the-art resin is not simply a 'Duet' of tradition and technology - it's a 'Plus' advantage indeed!",  # m description
                18900,  # m price
                1.2,  # kg
                [
                    'g-p19m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],


    # product 20 ----------------------------------------------------
    [
        "Hohner MÚSICA TÍPICA SERIES Accordion",  # product name
        8,  # brand id
        5,  # cate id - C
        47,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Hohner MÚSICA TÍPICA SERIES Accordion',  # model name
                'The typical HOHNER sound, as crisp and voluminous as we know it – but at an incredible price. The compadre is your best friend for your first steps into the world of Norteño, Tex-Mex, and folk punk. Explore the acoustic possibilities of Mexican, Irish, and German folk with this sturdy accordion designed for beginners and advanced players.',  # m description
                6400,  # m price
                2.2,  # kg
                [
                    'g-p20m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],


    # product 21 ----------------------------------------------------
    [
        "Yanaha MONTAGE8 Synthesizer",  # product name
        16,  # brand id
        5,  # cate id - C
        50,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yanaha MONTAGE8 Synthesizer',  # model name
                'MONTAGE 8 is an 88-key balanced hammer action synthesizer combining sophisticated dynamic control, massive sound creation and streamlined workflow',  # m description
                23000,  # m price
                4.5,  # kg
                [
                    'g-p21m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],


    # product 22 ----------------------------------------------------
    [
        "Roland SPD-SX Special Edition LaunchPad",  # product name
        17,  # brand id
        4,  # cate id - C
        48,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Roland SPD-SX Special Edition LaunchPad',  # model name
                'FOR PRO PLAYERS WHO NEED INSTANT ACCESS TO ALL THEIR ORIGINAL SOUNDS, WITHOUT COMPROMISE Roland s SPD-SX Sampling Pad is the professional touring standard for triggering custom samples, loops, and even complete backing tracks. It also supports real-time sample capture with its exclusive Multi-Pad Sampling function. The SPD-SX Special Edition is identical in functionality to the original SPD-SX, but features greatly expanded onboard storage. With 16 GB of internal memory available, its now possible to load enough studio-quality WAV samples to last an entire gig and beyond.',  # m description
                4700,  # m price
                1.4,  # kg
                [
                    'g-p22m1-1.jpg',
                    'g-p22m1-2.jpg',
                    'g-p22m1-3.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],


    # product 10 ----------------------------------------------------
    [
        "Yamaha AG01 Streaming Loopback Audio USB Microphone",  # product name
        16,  # brand id
        6,  # cate id - C
        51,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha AG01 Streaming Loopback Audio USB Microphone',  # model name
                'Configuring a streaming setup from scratch can be a daunting task, particularly for users with little production experience. The minimalist design of the AG01 takes this into account by combining a high-quality condenser microphone with DSP effects, a LOOPBACK function, flexible input connectivity, and a simple, intuitive mixer for stress-free streaming operation. Simply connect to your computer or iOS/Android device along with the headphones of your choice, then set your levels, and you ve got a fully operational streaming station. If you’re an aspiring live streamer that requires a compact yet comprehensive, high-quality, all-in-one solution, the AG01 is ready when you are.',  # m description
                2190,  # m price
                1,  # kg
                [
                    'g-p23m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],


    # product 10 ----------------------------------------------------
    [
        "Yamaha HPH-MT7W Studio Monitor Headphones",  # product name
        16,  # brand id
        6,  # cate id - C
        52,  # cate id - T
        54,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'Yamaha HPH-MT7W Studio Monitor Headphones',  # model name
                'High-resolution monitor headphones that reproduce even the most subtle nuances of the source sound. In addition to mixing and recording in the studio, the HPH-MT7W headphones are perfect for mix monitoring in live performance applications thanks to their high sound pressure levels and durability.',  # m description
                1200,  # m price
                0.8,  # kg
                [
                    'g-p24m1-1.jpg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    #
    # # product 10 ----------------------------------------------------
    # [
    #     "product-name-test",  # product name
    #     1,  # brand id
    #     1,  # cate id - C
    #     7,  # cate id - T
    #     53,  # cate id - A
    #     [  # model type list
    #         # model 1 ----------------------------------------------------------
    #         [
    #             'model-name-test',  # model name
    #             'model-description-test',  # m description
    #             100,  # m price
    #             2,  # kg
    #             [
    #                 'p1m1-1.png',
    #                 'p1m1-2.png',
    #                 'p1m1-3.png'
    #             ]
    #         ],
    #         # model 2 ----------------------------------------------------------
    #         # [],
    #         # model 3 ----------------------------------------------------------
    #         # []
    #     ]
    # ],

    #
    # # product 10 ----------------------------------------------------
    # [
    #     "product-name-test",  # product name
    #     1,  # brand id
    #     1,  # cate id - C
    #     7,  # cate id - T
    #     53,  # cate id - A
    #     [  # model type list
    #         # model 1 ----------------------------------------------------------
    #         [
    #             'model-name-test',  # model name
    #             'model-description-test',  # m description
    #             100,  # m price
    #             2,  # kg
    #             [
    #                 'p1m1-1.png',
    #                 'p1m1-2.png',
    #                 'p1m1-3.png'
    #             ]
    #         ],
    #         # model 2 ----------------------------------------------------------
    #         # [],
    #         # model 3 ----------------------------------------------------------
    #         # []
    #     ]
    # ],
]
