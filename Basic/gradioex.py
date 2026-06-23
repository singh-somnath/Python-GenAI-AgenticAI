import gradio as gr

def greet(msg):
    return msg.upper() 

demo = gr.Interface(
    fn=greet,
    inputs=[gr.Textbox(type="text",label="Your Message",lines=6)], 
    outputs=[gr.Textbox(lines=6)],
    allow_flagging="never").launch()

