import datetime
import time

class adventure:
    last_norm_clear = 11
    last_hell_clear = 9
    
    @staticmethod
    def start(mode="hell", chap=6, stage=8):
        click(wait("main_adventure.png", 10))

        control_mode = wait(Pattern("adventure_mode.png").similar(0.40), 10)
        click(control_mode.offset(Location(-60, -10)))
        click(control_mode.offset(Location(60, -10)))
        control_chap = wait(Pattern("adventure_chapter.png").similar(0.50), 3)
        control_stage = find(Pattern("adventure_stage.png").similar(0.40))
        
        if mode == "hell":
            click(control_mode.offset(Location(-60, -10)))
            click(control_mode.offset(Location(60, -10)))
            wait(0.5)
            for p in xrange(chap, adventure.last_hell_clear):
                click(control_chap.offset(Location(-170, 0)))
                wait(0.5)
        else:
            click(control_mode.offset(Location(40, -10)))
            click(control_mode.offset(Location(-40, -10)))
            wait(0.5)
            for p in xrange(chap, adventure.last_norm_clear):
                click(control_chap.offset(Location(-170, 0)))
                wait(0.5)
    
        if stage == 3:
            click(control_stage.offset(Location(-8, -166)))
        elif stage == 4:
            click(control_stage.offset(Location(-150, -10)))
        elif stage == 7:
            click(control_stage.offset(Location(147, -155)))
        elif stage == 8:
            click(control_stage.offset(Location(320, -150)))
    
        click(find(Pattern("adventure_repeat_on.png").similar(0.60)))
        click(find("adventure_start.png"))
        
        return angel.ADVENTURE

    @staticmethod
    def running():
        if exists(Pattern("adventure_status.png").similar(0.50), 5) is not None:
            getLastMatch().highlight(1)
            pass
        elif exists("stage_victory.png") is not None:
            try:
                click(find("adventure_restart.png"))
#                should check repeat mode is on
            except:
                pass
        elif exists("stage_defeat.png") is not None:
            click(find("adventure_restart.png"))
        else:
            return angel.UNIDENTIFIED

        return angel.ADVENTURE

class angel:
    UNIDENTIFIED, MAIN, ADVENTURE, FRIDGE, INTERSECTION, CHALLENGE = range(6)
    threshold = 0.50

    @staticmethod
    def check(state=ADVENTURE):
        if exists(Pattern("alarm_title.png").similar(0.90)) is not None:
            wait(5)

            if exists(Pattern("alarm_max_inven.png").similar(0.90), 0.1) is not None:
                getLastMatch().highlight(1)
                print "MAX INVENTORY"
                click(find(Pattern("alarm_ok.png").similar(0.90)))
                if exists(Pattern("inven_expand.png").similar(0.90), 1) is not None:
                    click(find(Pattern("alarm_close.png").similar(0.90)))
                    click(find(Pattern("back.png").similar(0.90)))
                angel.clear_inventory()
                return angel.MAIN
            elif exists(Pattern("alarm_no_energy.png").similar(0.90)) is not None:
                getLastMatch().highlight(1)
                if exists(Pattern("alarm_ok-1.png").similar(0.90)) is not None:
                    click(getLastMatch())
                elif exists(Pattern("alarm_no.png").similar(0.90)) is not None:
                    click(getLastMatch())
                    click(find(Pattern("back-1.png").similar(0.90)))
                angel.buy_energy()
                return angel.MAIN
        elif exists(Pattern("cafe_close.png").similar(0.90)) is not None:
            try:
                click(getLastMatch())
            except:
                pass
            return angel.UNIDENTIFIED
        elif exists(Pattern("popup_close.png").similar(0.90)) is not None:
            try:
                click(getLastMatch())
            except:
                pass
            return angel.UNIDENTIFIED
        elif exists(Pattern("back-2.png").similar(0.90)) is not None:
            getLastMatch().highlight(1)
            click(getLastMatch())
            return angel.UNIDENTIFIED

        if state == angel.UNIDENTIFIED:
            return angel.MAIN
        else:
            return state

    @staticmethod
    def clear_inventory():
        click(wait("main_char.png", 10))
        click(wait("inven_sell.png", 10))
        click(wait("inven_select_all.png", 3))

        wait(Pattern("inven_select_sell.png").similar(0.90), 5)
        click(find(Pattern("inven_select_2star.png").similar(0.90)))
        click(find(Pattern("inven_select_3star.png").similar(0.95)))
        click(find(Pattern("inven_select_4star.png").similar(0.95)))

        click(find(Pattern("inven_sell_all.png").similar(0.90)))
        if exists(Pattern("alarm_ok.png").similar(0.90), 2) is not None:
            click(getLastMatch())

        click(wait(Pattern("inven_go2item.png").similar(0.90), 10))
        wait(Pattern("inven_go2char.png").similar(0.90), 10)
        click(wait("inven_sell.png", 10))
        click(wait("inven_select_all.png", 3))

        wait(Pattern("inven_select_sell.png").similar(0.90), 5)
        click(find(Pattern("inven_select_2star.png").similar(0.90)))
        click(find(Pattern("inven_select_3star.png").similar(0.95)))
        click(find(Pattern("inven_select_4star.png").similar(0.95)))

        click(find(Pattern("inven_sell_all.png").similar(0.90)))
        if exists(Pattern("alarm_ok.png").similar(0.90), 2) is not None:
            click(getLastMatch())

        click(find(Pattern("back.png").similar(0.90)))
        return

    @staticmethod
    def buy_energy():
        
        click(find("shop_energy.png"))
        tab = wait(Pattern("shop_tab.png").similar(0.90), 3)

        while exists(Pattern("shop_gold2energy.png").similar(0.95)) is None:
            dragDrop(tab.below(300).right(50), tab.below(300).left(300))
            wait(0.5)

        for i in xrange(1):
            click(find(Pattern("shop_gold2energy.png").similar(0.95)))
            click(wait(Pattern("shop_gold2energy_confirm.png").similar(0.95), 3))
            if waitVanish(Pattern("shop_gold2energy_confirm.png").similar(0.95), FOREVER):
                continue
        click(find(Pattern("popup_close.png").similar(0.80)))
        return



setFindFailedResponse(ABORT)
setAutoWaitTimeout(1)

startTime = datetime.datetime.now()
popup(str(startTime))

state = angel.MAIN
mode, chap, stage = "hell", 8, 4
while True:
    state = angel.check(state)
    
    if state == angel.UNIDENTIFIED:
        continue
    elif state == angel.MAIN:
        state = adventure.start(mode, chap, stage)
        continue
    elif state == angel.ADVENTURE:
        state = adventure.running()
        continue
    elif state == angel.FRIDGE:
        pass

    print state
    wait(3)