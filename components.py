import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

import pandas as pd

jumbotron = dbc.Col(
    html.Div(
        [
            html.H2("Social Bart Behavioral DashBoard", className="display-3"),
            html.Hr(className="my-2"),
            html.P(
                ""
            ),
        ],
        className="h-100 p-5 text-white bg-dark rounded-3",
    ),
    md=12,
)

bg_markdown = dcc.Markdown('''
    ### Background.

    Howdy, here's some info about what is going on here. We have a bunch of "features"
    created when participants were playing a balloon game. How fun.

    Right, so when playing the game, players could press the spacebar on the computer to pump a virtual balloon. Each pump would reward the player 1 'token'.
    After pumping the balloon to a certain level (where ever the player felt comfortable pumping) the player could then 'cash' in their tokens by pressing the enter key.
    Upon doing this their token count for that balloon would be banked. Once they finished playing through all of their balloons they would then have one of their balloons
    selected at random and would be given a cash prize based on the token count for that individual balloon.

    But, alas, balloons do ***pop***. If the player popped a balloon before cashing it they would recieve 0 tokens for that balloon, and that balloon would be likewise be banked.
    This would increase the risk that when it came time for their payment, they would draw a balloon whose outcome was 0 tokens. And that is a bummer.

    Participants would play the game by themselves (how sad). With a computer (even more sad, though, same). Or with other people (How Lovely).
    These people that the players would play against were either from their same team, or from another team.

    The data here is organized both by "pump events" as well as by individual balloons that the player went through. So let's go ahead and define a "pump event".
    ''')
pump_event_info = dcc.Markdown('''
       #### Pump Events, and their features.

       A "pump event" in our case here is whenever the player pressed the spacebar. Players could either peck at the spacebar, skinner-box-pidgion style. Or,
       they could hold the spacebar down and accumulate pumps rapidly. For our purposes these "pump events" are treated the same. The only thing that will differ
       is the amount of pumps registered by one pump event.

       ##### Pump Event Features:

       Some of the features here are pump event features. The following table describes them, ish.
   ''')
pump_event_table_df = pd.DataFrame(
    {
        "Feature": ["pump_event_duration",
                    "onset_from_balloon_start",
                    "pump_event_pumps"],
        "Description": ["How long the spacebar was held down (in time)",
                        "When the spacebar was pressed (in time) relative to the start of the balloon.",
                        "How many pumps were registered during this pump event. i.e. If they started at 9 and pumped until 20 -> pump_event_pumps == 20"],
        "Units": ["seconds",
                  "seconds",
                  "pumps"]
    }
    )
pump_event_table = dbc.Table.from_dataframe(pump_event_table_df , striped=True, bordered=True, hover=True)
balloon_event_info = dcc.Markdown('''
    ##### Balloon Features:

    Other than pump event features, there are also **balloon wise** features. i.e. these features are broken
    down at the indiviaul balloon level. When looking over these features recognize that the number of samples
    should be equal to `count(id) * count(number_of_balloons[id])`

    The table to the right should describe these features.
''')
balloon_table_df = pd.DataFrame(
    {
        "Feature": ["total_balloon_duration",
                    "total_pumps_for_balloon",
                    "number_of_pump_actions",
                    "balloon_pop_point"],
        "Description": ["How long the balloon (trial) lasted (in time)",
                        "How many total ... pumps ... there ... were for the balloon?",
                        "How many individual pump actions there were for the balloon, i.e. if I pumped from 0 - 9 and then 9 - 22. That is two pump actions.",
                        "The underlying pop point (this is computer generated, and was not knowable to the player)."],
        "Units": ["seconds",
                  "pumps",
                  "actions",
                  "pumps"]
    }
    )
balloon_table = dbc.Table.from_dataframe(balloon_table_df , striped=True, bordered=True, hover=True)
grouping_event_info = dcc.Markdown('''
       ##### Grouping Features
       There are some other features of the balloon that would not make much sense to plot (as they are categorical). Here they are.
   ''')
grouping_event_table_df = pd.DataFrame(
    {
        "Feature": ["game_condition",
                    "balloon_outcome",
                    "game_opponent"],
        "Description": ["What type of game this was. Aka, who they player was up against",
                        "... the outcome of the balloon (I did a got variable name there)",
                        "The ID to the opponent player (or 0, 1 for solo / computer opponent)"],
        "Values": ["Solo, Computer Opponent, Human Opponent",
                   "Popped, Cashed",
                   "a unique ID"]
    }
    )
grouping_event_table = dbc.Table.from_dataframe(grouping_event_table_df , striped=True, bordered=True, hover=True)

background = dbc.Row(
    dbc.Col(bg_markdown, width=12)
)

pump_event = dbc.Row(
    [dbc.Col(pump_event_info, width=6),
    dbc.Col(pump_event_table, width=6),]
)

balloon_event = dbc.Row(
    [dbc.Col(balloon_event_info, width=6),
    dbc.Col(balloon_table, width=6),]
)

grouping_event = dbc.Row(
    [dbc.Col(grouping_event_info, width=6),
    dbc.Col(grouping_event_table, width=6),]
)

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    background
                ],
                title="General Background Information About the Data",
            ),
            dbc.AccordionItem(
                [
                    pump_event
                ],
                title="Pump Event Background Information",
            ),
            dbc.AccordionItem(
                [
                    balloon_event
                ],
                title="Balloon Event Background Information"
            ),
            dbc.AccordionItem(
                [
                    grouping_event
                ],
                title="Grouping Variables Background Information"
            ),
        ],
        start_collapsed=True
    )
)
