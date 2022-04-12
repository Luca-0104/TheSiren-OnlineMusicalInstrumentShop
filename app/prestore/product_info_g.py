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
                    'g-p4m1-1.png',
                    'g-p4m1-2.png'
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
                    'g-p5m1-1.jpg',
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
                    'g-p5m2-1.jpg',
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
                    'g-p5m3-1.jpg',
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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

    # product 10 ----------------------------------------------------
    [
        "product-name-test",  # product name
        1,  # brand id
        1,  # cate id - C
        7,  # cate id - T
        53,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'model-name-test',  # model name
                'model-description-test',  # m description
                100,  # m price
                2,  # kg
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
]
