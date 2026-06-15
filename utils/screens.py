from utils.constants import CANVAS_WIDTH

def draw_start_screen(canvas, play_label, on_play, on_highscore, on_exit):
    title = canvas.create_text(CANVAS_WIDTH // 2, 150, text="Brick Breaker", font=("Arial", 42, "bold"), fill="WHITE")
    play_text = canvas.create_text(CANVAS_WIDTH // 2, 300, text=play_label, font=("Arial", 20), fill="WHITE")
    highscore_text = canvas.create_text(CANVAS_WIDTH // 2, 360, text="High Score", font=("Arial", 20), fill="WHITE")
    exit_text = canvas.create_text(CANVAS_WIDTH // 2, 420, text="Exit", font=("Arial", 20), fill="WHITE")

    canvas.tag_bind(play_text, "<Button-1>", on_play)
    canvas.tag_bind(highscore_text, "<Button-1>", on_highscore)
    canvas.tag_bind(exit_text, "<Button-1>", on_exit)

    return [title, play_text, highscore_text, exit_text]

def draw_transition_screen(canvas, displayed, on_next, on_save_exit):
    title = canvas.create_text(CANVAS_WIDTH // 2, 150, text=displayed, font=("Arial", 42, "bold"), fill="WHITE")
    continue_text = canvas.create_text(CANVAS_WIDTH // 2, 300, text="Next Level", font=("Arial", 20), fill="WHITE")
    save_exit_text = canvas.create_text(CANVAS_WIDTH // 2, 420, text="Save and Exit", font=("Arial", 20), fill="WHITE")

    canvas.tag_bind(continue_text, "<Button-1>", on_next)
    canvas.tag_bind(save_exit_text, "<Button-1>", on_save_exit)

    return [title, continue_text, save_exit_text]

def draw_game_over_screen(canvas, title_text, on_play_again, on_exit): 
    title = canvas.create_text(CANVAS_WIDTH // 2, 150, text=title_text, font=("Arial", 42, "bold"), fill="WHITE")
    play_again_text = canvas.create_text(CANVAS_WIDTH // 2, 300, text="Play Again", font=("Arial", 20), fill="WHITE")
    exit_text = canvas.create_text(CANVAS_WIDTH // 2, 420, text="Exit", font=("Arial", 20), fill="WHITE")

    canvas.tag_bind(play_again_text, "<Button-1>", on_play_again)
    canvas.tag_bind(exit_text, "<Button-1>", on_exit)

    return [title, play_again_text, exit_text]