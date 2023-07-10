import os
from random import choice
from time import sleep
import vizdoom as vzd
import psutil
import matplotlib.pyplot as plt
if __name__ == "__main__":
    game = vzd.DoomGame()
    game.set_doom_scenario_path(os.path.join(vzd.scenarios_path, "basic.wad"))
    game.set_doom_map("map01")
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    game.set_screen_format(vzd.ScreenFormat.RGB24)
    game.set_depth_buffer_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)
    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)  
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False) 
    game.set_render_particles(False)
    game.set_render_effects_sprites(False) 
    game.set_render_messages(False) 
    game.set_render_corpses(False)
    game.set_render_screen_flashes(True)

    game.set_available_buttons([vzd.Button.MOVE_LEFT, vzd.Button.MOVE_RIGHT, vzd.Button.ATTACK])

    print("Available buttons:", [b.name for b in game.get_available_buttons()])
    game.set_available_game_variables([vzd.GameVariable.AMMO2])
    print("Available game variables:", [v.name for v in game.get_available_game_variables()])

    game.set_episode_timeout(200)
    game.set_episode_start_time(10)
    game.set_window_visible(True)

    game.set_living_reward(-1)

    game.set_mode(vzd.Mode.PLAYER)

    game.init()

    actions = [[True, False, False], [False, True, False], [False, False, True]]
    episodes = 2

    sleep_time = 1.0 / vzd.DEFAULT_TICRATE  # = 0.028

    cpu_usage = []
    memory_usage = []
    for i in range(episodes):
        print(f"Episode #{str(i + 1)}")

        game.new_episode()

        while not game.is_episode_finished():

            # Gets the state
            state = game.get_state()

            # Which consists of:
            n = state.number
            vars = state.game_variables
            screen_buf = state.screen_buffer
            depth_buf = state.depth_buffer
            labels_buf = state.labels_buffer
            automap_buf = state.automap_buffer
            labels = state.labels
            objects = state.objects
            sectors = state.sectors

            r = game.make_action(choice(actions))
            cpu_usage.append(psutil.Process(os.getpid()).cpu_percent())
            memory_usage.append(psutil.Process(os.getpid()).memory_percent())

            print(f"State #{str(n)}")
            print("Game variables:", vars)
            print("Reward:", r)
            print("=====================")

            if sleep_time > 0:
                sleep(sleep_time)

        print("Episode finished.")
        print("Total reward:", game.get_total_reward())
        print("************************")
    game.close()
    cpu_plot = plt.plot(cpu_usage)
    plt.title("CPU usage")
    plt.show()
    memory_plot = plt.plot(memory_usage)
    plt.title("Memory usage")
    plt.show()
    for cpu in cpu_usage:
        print(f"CPU usage: {cpu}%")
    for memory in memory_usage:
        print(f"Memory usage: {memory}%")