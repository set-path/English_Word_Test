import gradio as gr
import json
import numpy as np
import datetime

def load_javascript():
    GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse
    print("loading javascript...")
    js = '''
    <script src="file=custom.js"></script>
    '''

    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</html>', f'{js}</html>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response

class Englisg:
    def __init__(self) -> None:
        self.data = json.load(open('data.json','r',encoding='utf8'))
        self.cur_index = -1

    def start(self):
        self.index = np.random.choice(list(range(0,len(self.data))),len(self.data),replace=False)
        self.cur_index = 0
        self.show_english = np.random.choice(list(range(0,len(self.data))),len(self.data)//2,replace=False)
        self.success = 0
        self.remaining = len(self.data)
    
        if self.index[self.cur_index] in self.show_english:
            return self.data[self.index[self.cur_index]]['english'],f"Success: {self.success}",f"Remaining: {self.remaining}",""
        else:
            return self.data[self.index[self.cur_index]]['chinese'],f"Success: {self.success}",f"Remaining: {self.remaining}",""
    
    def eval(self,answer):
        if self.index[self.cur_index] in self.show_english:
            if answer == self.data[self.index[self.cur_index]]['chinese']:
                self.success += 1
                self.remaining -= 1
                self.cur_index += 1
                if self.success == len(self.data):
                    return "Congratulations! You have finished all the questions!","",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
                if self.index[self.cur_index] in self.show_english:
                    return self.data[self.index[self.cur_index]]['english'],"",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
                else:
                    return self.data[self.index[self.cur_index]]['chinese'],"",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
            else:
                if self.index[self.cur_index] in self.show_english:
                    return self.data[self.index[self.cur_index]]['english'],answer,f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Wrong\n"
                else:
                    return self.data[self.index[self.cur_index]]['chinese'],answer,f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Wrong\n"
        else:
            if answer.lower() == self.data[self.index[self.cur_index]]['english'].lower():
                self.success += 1
                self.remaining -= 1
                self.cur_index += 1
                if self.success == len(self.data):
                    return "Congratulations! You have finished all the questions!","",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
                if self.index[self.cur_index] in self.show_english:
                    return self.data[self.index[self.cur_index]]['english'],"",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
                else:
                    return self.data[self.index[self.cur_index]]['chinese'],"",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Correct\n"
            else:
                if self.index[self.cur_index] in self.show_english:
                    return self.data[self.index[self.cur_index]]['english'],answer,f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Wrong\n"
                else:
                    return self.data[self.index[self.cur_index]]['chinese'],answer,f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Wrong\n"

    def show(self):
        if self.index[self.cur_index] in self.show_english:
            return self.data[self.index[self.cur_index]]['chinese']
        else:
            return self.data[self.index[self.cur_index]]['english']
        
    def save(self):
        if self.cur_index == -1:
            return
        res = {}
        res['success'] = self.success
        res['remaining'] = self.remaining
        res['cur_index'] = self.cur_index
        res['index'] = self.index.tolist()
        res['show_english'] = self.show_english.tolist()
        config_filename = f"config_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        with open(config_filename,'w',encoding='utf8') as f:
            json.dump(res,f,ensure_ascii=False,indent=4)
        return f"Info: Saved to {config_filename}\n"
    
    def load_config(self,config):
        config = json.load(open(config.name,'r',encoding='utf8'))
        self.cur_index = config['cur_index']
        self.success = config['success']
        self.remaining = config['remaining']
        self.index = np.array(config['index'])
        self.show_english = np.array(config['show_english'])
        if self.index[self.cur_index] in self.show_english:
            return self.data[self.index[self.cur_index]]['english'],f"Success: {self.success}",f"Remaining: {self.remaining}",""
        else:
            return self.data[self.index[self.cur_index]]['chinese'],f"Success: {self.success}",f"Remaining: {self.remaining}",""
        
english = Englisg()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=4):
            question = gr.Textbox(lines=1, label="Question", interactive=False)
            answer = gr.Textbox(lines=1, label="Answer",elem_id="user-input")
            info = gr.Text(lines=5,label="Info", interactive=False)
            start_btn = gr.Button(value="Start",variant="primary",elem_id="start-btn")
            show_answer_btn = gr.Button(value="Show Answer",elem_id="show-answer-btn")
            submit_btn = gr.Button(value="Submit",elem_id="submit-btn")
            save_btn = gr.Button(value="Save",elem_id="save-btn")
        with gr.Column(scale=1):
            success = gr.Label(value="Success: 0",show_label=False)
            remaining = gr.Label(value="Remaining: 0",show_label=False)
            load_config = gr.File(label="Load Config",type="file",file_count='single')
    
    start_btn.click(english.start,outputs=[question,success,remaining,info])
    show_answer_btn.click(english.show,outputs=[info])
    submit_btn.click(english.eval,inputs=[answer],outputs=[question,answer,success,remaining,info])
    save_btn.click(english.save,outputs=[info])
    load_config.upload(english.load_config,inputs=[load_config],outputs=[question,success,remaining])

load_javascript()
demo.queue(concurrency_count=4).launch(inbrowser=True)