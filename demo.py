import gradio as gr
import json
import numpy as np
import datetime
import os

def load_javascript():
    GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse
    print("loading javascript...")
    js = '''
    <script src="file=js/custom.js"></script>
    '''

    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</html>', f'{js}</html>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response

data_file = [file for file in os.listdir('data/') if file.endswith('.json')]

class Englisg:
    def __init__(self) -> None:
        self.cur_index = -1
        self.success = 0
        self.remaining = 0
        self.data_file = ""
        self.data = []
        self.index = []
        self.show_english = []
        self.error_index = []

    def start(self,data_file):
        self.data_file = data_file
        self.data = json.load(open(f'data/{data_file}','r',encoding='utf8'))
        self.error_index = []
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
        if self.cur_index == -1:
            return "","",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Please start first!"
        if self.index[self.cur_index] in self.show_english:
            if answer == self.data[self.index[self.cur_index]]['chinese']:
                self.success += 1
                self.remaining -= 1
                self.cur_index += 1
                if self.success == len(self.data):
                    self.cur_index = -1
                    return "","",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Congratulations! You have finished all the questions!\n"
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
                    self.cur_index = -1
                    return "","",f"Success: {self.success}",f"Remaining: {self.remaining}",f"Info: Congratulations! You have finished all the questions!\n"
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
        if self.cur_index == -1:
            return "Please start first!"
        if self.index[self.cur_index] not in self.error_index:
            self.error_index.append(self.index[self.cur_index])
        if self.index[self.cur_index] in self.show_english:
            return self.data[self.index[self.cur_index]]['chinese']
        else:
            return self.data[self.index[self.cur_index]]['english']
        
    def save(self):
        if self.cur_index == -1 and len(self.error_index) == 0:
            return "Please start first!"
        files = []
        suffix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if self.cur_index != -1:
            res = {}
            res['data_file'] = self.data_file
            res['success'] = self.success
            res['remaining'] = self.remaining
            res['cur_index'] = self.cur_index
            res['index'] = self.index.tolist()
            res['show_english'] = self.show_english.tolist()
            config_filename = f"config_{suffix}.json"
            with open(f'config/{config_filename}','w',encoding='utf8') as f:
                json.dump(res,f,ensure_ascii=False,indent=4)
            files.append(f"config_{suffix}.json")
        if len(self.error_index) != 0:
            error_data = np.array(self.data)[self.error_index].tolist()
            error_filename = f"error_{len(error_data)}_{suffix}.json"
            with open(f'data/{error_filename}','w',encoding='utf8') as f:
                json.dump(error_data,f,ensure_ascii=False,indent=4)
            files.append(f"error_{len(error_data)}_{suffix}.json\n")
        if len(files) == 0:
            return "Info: Nothing to save!"
        return "Info: Save as " + " and ".join(files) + "\n"
    
    def load_config(self,config):
        config = json.load(open(config.name,'r',encoding='utf8'))
        self.data_file = config['data_file']
        self.data = json.load(open(f'data/{self.data_file}','r',encoding='utf8'))
        self.error_index = []
        self.cur_index = config['cur_index']
        self.success = config['success']
        self.remaining = config['remaining']
        self.index = np.array(config['index'])
        self.show_english = np.array(config['show_english'])
        if self.index[self.cur_index] in self.show_english:
            return self.data[self.index[self.cur_index]]['english'],f"Success: {self.success}",f"Remaining: {self.remaining}",self.data_file
        else:
            return self.data[self.index[self.cur_index]]['chinese'],f"Success: {self.success}",f"Remaining: {self.remaining}",self.data_file
    
    def refresh(self):
        data_file = [file for file in os.listdir('data/') if file.endswith('.json')]
        return gr.update(choices=data_file,value=data_file[0])

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
            data_file_dropdown = gr.Radio(label="Data File",choices=data_file,value=data_file[0])
            refresh_btn = gr.Button(value="Refresh")
            load_config = gr.File(label="Load Config",type="file",file_count='single')
    
    start_btn.click(english.start,inputs=[data_file_dropdown],outputs=[question,success,remaining,info])
    show_answer_btn.click(english.show,outputs=[info])
    submit_btn.click(english.eval,inputs=[answer],outputs=[question,answer,success,remaining,info])
    save_btn.click(english.save,outputs=[info])
    refresh_btn.click(english.refresh,outputs=[data_file_dropdown])
    load_config.upload(english.load_config,inputs=[load_config],outputs=[question,success,remaining,data_file_dropdown])

load_javascript()
demo.queue(concurrency_count=4).launch(inbrowser=True)