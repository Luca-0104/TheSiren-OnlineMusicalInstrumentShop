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
    # product 0 ----------------------------------------------------
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
    [
        "YPC-87",  # product name
        16,  # Yamaha
        2,  # cate id - C Woodwinds
        22,  # cate id - T
        56,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'YPC-87R',  # model name
                'The bright, nimble addition to the Yamaha piccolo family',  # m description
                17500,  # m price
                1.5,  # kg
                [
                    'l-p1m1-1.jpg',
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'YPC-87',  # model name
                'The Yamaha Piccolo subverts the traditional exterior design with a strikingly gorgeous shape. This professional wood piccolo is crafted from carefully-seasoned ebony wood for a brilliant, bright tone with the soft, full sound of a wood piccolo.',  # m description
                11800,  # m price
                1.5,  # kg
                [
                    'l-p1m1-1.jpg',
                ]
            ],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 2 ----------------------------------------------------
    [
        "YPC-32",  # product name
        16,  # Yamaha
        2,  # cate id - C Woodwinds
        22,  # cate id - T
        56,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'YPC-32',  # model name
                'Due to its ease of play, it has precise intonation and a characteristic piccolo sound. YPC-32 is very popular among students. The body of the flute is made of durable ABS resin, and the sound is similar to that of a wooden piccolo.',  # m description
                8100,  # m price
                1.3,  # kg
                [
                    'l-p2m1-1.jpg',
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
        "YPC-82",  # product name
        16,  # Yamaha
        2,  # cate id - C Woodwinds
        22,  # cate id - T
        56,  # cate id - A
        [  # model type list
            # model 1 ----------------------------------------------------------
            [
                'YPC-82',  # model name
                'These piccolos are handcrafted by skilled craftsmen and are made of ebony. The YPC-82 comes with a sterling silver flute head',  # m description
                22800,  # m price
                1.4,  # kg
                [
                    'l-p3m1-1.jpeg',
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
        "YPC-91",        # product name
        16,                          # brand id
        2,                          # cate id - C
        22,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'YPC-91',          # model name
                "Handcrafted by skilled craftsmen in collaboration with some of the world's musicians, the YPC-91 features a selection of dried ebony wood on both the head and body of the flute.",   # m description
                67600,                        # m price
                2,                          # kg
                [
                    'l-p4m1-1.jpeg'
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
        "YPC-92",        # product name
        16,                          # brand id
        2,                          # cate id - C
        22,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'YPC-92',          # model name
                "Handcrafted by skilled craftsmen in collaboration with some of the world's musicians, the YPC-92 features a selection of dried ebony wood on both the head and body of the flute.",   # m description
                77600,                        # m price
                2,                          # kg
                [
                    'l-p5m1-1.jpeg'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 6 ----------------------------------------------------
    [
        "ALTO 8101",        # product name
        6,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'ALTO 8101',          # model name
                'The 100 Series alto and tenor saxophones provide students with immediate, affordable quality.',   # m description
                14500,                        # m price
                6,                          # kg
                [
                    'l-p6m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 7 ----------------------------------------------------
    [
        "SENZO",        # product name
        6,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'SENZO',          # model name
                'Senzo announces the rebirth of Buffet Crampon’s professional saxophones. Senzo, which means ancestor in Japanese, combines Buffet Crampon’s tradition of musical excellence with a sensual and modern approach.',   # m description
                27500,                        # m price
                7,                          # kg
                [
                    'l-p7m1-1.png',
                    'l-p7m1-2.png',
                    'l-p7m1-3.png',
                    'l-p7m1-4.png'
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
        "TENOR 8102",        # product name
        6,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'TENOR 8102',          # model name
                'The 100 Series alto and tenor saxophones provide students with immediate, affordable quality.',   # m description
                28500,                        # m price
                6.5,                          # kg
                [
                    'l-p8m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 9 ----------------------------------------------------
    [
        "ALTO 400 SERIES",        # product name
        6,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'ALTO 400 SERIES',          # model name
                'The 400 Series is designed for the advanced student through the professional saxophonist.',   # m description
                37500,                        # m price
                6.5,                          # kg
                [
                    'l-p9m1-1.png'
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
        "BARITONE 400 SERIES",        # product name
        6,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'BARITONE 400 SERIES',          # model name
                'The 400 Series is designed for the advanced student through the professional saxophonist.',   # m description
                28500,                        # m price
                8,                          # kg
                [
                    'l-p10m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            # [],
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

    # product 11 ----------------------------------------------------
    [
        "YBS-480",        # product name
        16,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'YBS-480',          # model name
                'Yamaha upper bass saxophone is known worldwide for its outstanding sound quality. The Yamaha YBS-480 refreshes the traditional image of the Yamaha upper bass saxophone with its powerful and exquisite timbre and excellent playability. The improved flare configuration and button layout make grips more comfortable and pitch stable, making it ideal for beginners with bass saxophone.',   # m description
                62000,                        # m price
                8,                          # kg
                [
                    'l-p11m1-1.png'
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
        "YBS-62II",        # product name
        16,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'YBS-62II',          # model name
                'Since the release of the Yamaha 62 series professional saxophone for more than 40 years, it has been well received and favored by players around the world. The new YBS-62II Professional Upper Bass Saxophone, with its excellent blowpigability inherited from the custom series, strikes the perfect balance in the design of professional-grade instruments.',   # m description
                84000,                        # m price
                7.5,                          # kg
                [
                    'l-p12m1-1.png'
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
        "YBS-82",        # product name
        16,                          # brand id
        2,                          # cate id - C
        23,                          # cate id - T
        56,                         # cate id - A
        [                           # model type list
            # model 1 ----------------------------------------------------------
            [
                'YBS-82',          # model name
                "Yamaha's first custom upper bass saxophone YBS-82, with years of experience in instrument development, brings a new standard to the design of the upper bass saxophone. The YBS-82 caters to players who aspire to timbre, adding timbre brightness to the thick upper bass range and treble range. The YBS-82 is not just a bass instrument, but also a diversity of performances as a soloist.",   # m description
                116000,                        # m price
                7,                          # kg
                [
                    'l-p12m1-1.png'
                ]
            ],
            # model 2 ----------------------------------------------------------
            [
                'YBS-82 WOF',  # model name
                "Yamaha's first custom upper bass saxophone YBS-82, with years of experience in instrument development, brings a new standard to the design of the upper bass saxophone. The YBS-82 caters to players who aspire to timbre, adding timbre brightness to the thick upper bass range and treble range. The YBS-82 is not just a bass instrument, but also a diversity of performances as a soloist.",
                # m description
                116000,  # m price
                7,  # kg
                [
                    'l-p12m1-1.png',
                    'l-p12m2-1.png'

                ]
            ]
            # model 3 ----------------------------------------------------------
            # []
        ]
    ],

# product 0 ----------------------------------------------------
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

# product 0 ----------------------------------------------------
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

# product 0 ----------------------------------------------------
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

# product 0 ----------------------------------------------------
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

# product 0 ----------------------------------------------------
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
]




































