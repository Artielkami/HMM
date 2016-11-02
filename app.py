try:
    import Tkinter as tk
    import tkFont
except ImportError:
    import tkinter as tk
    import tkinter.font as tkFont
import sys
import tkMessageBox as tkmsg
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import ConfigParser
from viterbi import *
import math as math
import yaml as Yaml
from sup import my_calendar as Cal
import read_data_price as rdp
import time

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[APP]: %(message)s')
# import calendar


class Dialog(tk.Tk):

    def __init__(self, setting, data, *args, **kwargs):

        self.master = tk.Tk.__init__(self, *args, **kwargs)
        self.title(setting['title'])
        self.geometry(setting['geometry'])
        self.vcmd_float = (self.register(self._on_validate_float),
                           '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # frame
        self.form_frame = tk.LabelFrame(master=self.master, text='Form master', **kwargs)
        self.form_frame.grid(row=0, column=0, columnspan=2, sticky='we', padx=10, pady=5)
        self.left_frame = tk.Frame(master=self.master, **kwargs)
        self.left_frame.grid(row=1, column=0)
        self.right_frame = tk.Frame(master=self.master, **kwargs)
        self.right_frame.grid(row=1, column=1, sticky=tk.NW)
        self.input_frame = tk.Frame(master=self.master, **kwargs)
        self.input_frame.grid(row=2, column=0, sticky=tk.NW, columnspan=2)
        self.bottom_frame = tk.LabelFrame(master=self.master, text='Result', height=250, **kwargs)
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky='we', padx=10, pady=5)
        # variable for calculate
        self.matrix_transit = [
            [0.23, 0.32, 0.45],
            [0.30, 0.30, 0.40],
            [0.36, 0.38, 0.26]
        ]
        self.matrix_emission = [
            [0.584, 0.416],
            [0.52, 0.48],
            [0.34, 0.66]
        ]
        self.matrix_tp = []
        self.matrix_ep = []
        # print self.matrix_transit
        # print self.matrix_emission
        # print '-----------'
        self.port_dep = tk.StringVar(self.master)
        self.port_dep.set('TYOA')

        self.port_des = tk.StringVar(self.master)
        self.port_des.set('ISG or MMY')

        self.day_out = tk.StringVar(self.master)
        self.day_out.set('2016-12-09')

        self.day_in = tk.StringVar(self.master)
        # self.day_in.set('')

        # self.log_text = None

        self.result_text = tk.StringVar(self.master)
        self.result_text.set('Ready for calculation')

        self.old_status = tk.StringVar(self.master)
        self.old_status.set(data['old_status'])

        self.new_state = None

        # self.old_prob = tk.DoubleVar(self.master)
        # self.old_prob.set(data['old_prob'])

        self.old_DS = tk.IntVar(self.master)
        self.old_DS.set(data['old_DS'])

        self.new_DS = tk.IntVar(self.master)
        self.new_DS.set(data['new_DS'])

        self.old_CR = tk.IntVar(self.master)
        self.old_CR.set(data['old_CR'])

        self.new_CR = tk.IntVar(self.master)
        self.new_CR.set(data['new_CR'])

        self.old_price = tk.DoubleVar(self.master)
        self.old_price.set(data['old_price'])

        # GUI render

        self._master_frame(self.form_frame)
        self._TpFrame(self.left_frame)
        self._TeFrame(self.left_frame)
        self._ImportButton(self.right_frame)
        self._InputFrame(self.input_frame)
        self._ResultFrame(self.bottom_frame)

        # Read setting
        self._read_setting()
        self.session = None
        # --------------------------------------------------------------------------------------------------------------
        #
        #   MENU
        #
        # --------------------------------------------------------------------------------------------------------------
        menu = tk.Menu(self)
        self.config(menu=menu)

        # File menu
        # Import config, Import data
        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        # filemenu.add_command(label="New", command=self.NewFile)
        # filemenu.add_command(label="Open...", command=self.OpenFile)
        filemenu.add_command(label='Import config', command=self.import_transit_prob)
        filemenu.add_command(label='Change data root folder', command=self._write_setting)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        # Tool menu
        # Clear
        toolmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Tool', menu=toolmenu)
        # clear log result
        toolmenu.add_command(label='Clear log', command=self.clear_log_result)
        toolmenu.add_command(label='Create Session', command=self.get_live_data)
        toolmenu.add_command(label='Get Data', command=self.get_data)
        toolmenu.add_command(label='Test', command=self.test)

        # Help
        # Help, About
        helpmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

    def calculate_prob(self):
        self._get_value_transit()
        self._get_value_emission()
        obs = []
        if self.new_DS.get() - self.old_DS.get() >= 0:
            obs.append('DS_increase')
        else:
            obs.append('DS_decrease')
        states = ('Price_up', 'Price_keep', 'Price_down')

        start_probability = dict()
        for s in states:
            if s == self.old_status.get():
                # if self.old_prob.get() < 0.005:
                #     start_probability[s] = self.old_prob.get()*100
                # else:
                #     start_probability[s] = self.old_prob.get()
                start_probability[s] = 1
            else:
                start_probability[s] = 0
        tran_prob = {
            'Price_up': {'Price_up': self.matrix_transit[0][0],
                         'Price_keep': self.matrix_transit[0][1],
                         'Price_down': self.matrix_transit[0][2]},
            'Price_keep': {'Price_up': self.matrix_transit[1][0],
                           'Price_keep': self.matrix_transit[1][1],
                           'Price_down': self.matrix_transit[1][2]},
            'Price_down': {'Price_up': self.matrix_transit[2][0],
                           'Price_keep': self.matrix_transit[2][1],
                           'Price_down': self.matrix_transit[2][2]}
        }
        emission_prob = {
            'Price_up': {'DS_increase': self.matrix_emission[0][0], 'DS_decrease': self.matrix_emission[0][1]},
            'Price_keep': {'DS_increase': self.matrix_emission[1][0], 'DS_decrease': self.matrix_emission[1][1]},
            'Price_down': {'DS_increase': self.matrix_emission[2][0], 'DS_decrease': self.matrix_emission[2][1]}
        }
        v = Viterbi()
        rs = v.calculate(obs=obs, states=states, start_p=start_probability, trans_p=tran_prob, emit_p=emission_prob)
        text = '---------------\n'
        for key, value in rs.items():
            text += key + ' : ' + str(value['prob']) + '\n'
        text += '---------------'
        max_prob = max(value["prob"] for key, value in rs.items())
        state = ''
        for st, data in rs.items():
            if data["prob"] == max_prob:
                # opt.append(st)
                state = st
                self.new_state = st
                break
        text += '\n=> Next states will be : ' + state

        new_ds = self.new_DS.get()
        old_ds = self.old_DS.get()
        delta = new_ds - old_ds + 1
        base = delta*new_ds*old_ds
        if delta == 1:
            x = math.log(new_ds, 888)
        # x = float(old_ds+1.4*abs(delta)+1)/float(new_ds+1)
        else:
            x = (float(new_ds)+1)/(float(old_ds)+1)
        h = math.log(x, base)
        old_price = self.old_price.get()
        new_price = 0
        if state == 'Price_down':
            new_price = old_price*(1-abs(h))
        elif state == 'Price_up':
            new_price = old_price*(1+abs(h))
        else:
            new_price = old_price
        text += '\n' + str(new_price)
        self.result_text.set(text)

    def _on_validate_float(self, action, index, value_if_allowed,
                           prior_value, text, validation_type, trigger_type, widget_name):
        # if text in '0123456789.':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                if not value_if_allowed:
                    return True
                print '-fail 1-'
                return False
        # else:
        #     print '-fail 2-'
        #     return False

    def _get_value_transit(self):
        try:
            for index, item in enumerate(self.matrix_tp):
                row = index // 3
                col = index % 3
                self.matrix_transit[row][col] = float(item.get())
            # print self.matrix_transit
        except ValueError:
            print 'Error input value'
        # print '---'

    def _get_value_emission(self):
        try:
            for index, item in enumerate(self.matrix_ep):
                row = index // 2
                col = index % 2
                self.matrix_emission[row][col] = float(item.get())
            # print self.matrix_emission
        except ValueError:
            print 'Error input value'
        # print '---'

    def _TpFrame(self, master=None, **kwargs):
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        f = tk.Frame(self.frame, **kwargs)
        f.pack(fill=tk.X)
        w = tk.Label(f, text="Table transits probability", fg="blue", anchor=tk.W, justify=tk.LEFT)
        w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # w.grid(row=0, column=0,)
        # make table transit probability
        g = tk.Frame(self.frame, **kwargs)
        g.pack(fill=tk.X, side=tk.LEFT)
        # f.grid(row=1, column=0)
        for i in range(1, 4, 1):
            for j in range(0, 3, 1):
                w = tk.Entry(g, validate='key', validatecommand=self.vcmd_float)
                w.insert(0, self.matrix_transit[i-1][j])
                w.grid(row=i, column=j)
                self.matrix_tp.append(w)

    def _TeFrame(self, master=None, **kwargs):
        # frame table + label
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10)
        # frame for label
        f = tk.Frame(self.frame, **kwargs)
        f.pack(fill=tk.X)
        w = tk.Label(f, text="Table emission probability", fg="blue", anchor=tk.W, justify=tk.LEFT)
        w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # frame for table
        g = tk.Frame(self.frame, **kwargs)
        g.pack(fill=tk.X)
        # make table transit probability
        for i in range(1, 4, 1):
            for j in range(0, 2, 1):
                w = tk.Entry(g, validate='key', validatecommand=self.vcmd_float)
                w.insert(0, self.matrix_emission[i-1][j])
                w.grid(row=i, column=j)
                self.matrix_ep.append(w)

    def _ImportButton(self, master=None, **kwargs):
        # frame table + label
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # w = tk.Label(self.frame, text="Table emission probability", fg="blue", justify=tk.LEFT)
        # w.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        b = tk.Button(self.frame, text="In transit", bg="green", height=7, padx=5, width=10,
                      activebackground='blue', command=self._get_value_transit)
        b.grid(row=0, column=0)
        b = tk.Button(self.frame, text="Read data", bg="yellow", height=7, width=10, padx=5,
                      activebackground='blue', command=self.import_doto)
        b.grid(row=0, column=1)
        b = tk.Button(self.frame, text="In emission", bg="green", height=7, width=10, padx=5,
                      activebackground='blue', command=self._get_value_emission)
        b.grid(row=1, column=0)
        b = tk.Button(self.frame, text="Calculate", bg="red", height=7, width=10, padx=5,
                      activebackground='blue', command=self.calculate_prob)
        b.grid(row=1, column=1)

    def _InputFrame(self, master=None, **kwargs):
        self.frame = tk.Frame(master=master, **kwargs)
        self.frame.pack(fill=tk.X, padx=10, pady=10, side=tk.LEFT)
        # 1
        w = tk.Label(self.frame, text="Old status", fg="blue", justify=tk.LEFT)
        w.grid(row=0, column=0)
        h = tk.Entry(self.frame, width=17, textvariable=self.old_status)
        h.grid(row=1, column=0)

        # 2
        # w = tk.Label(self.frame, text="Old probability", fg="blue", justify=tk.LEFT)
        # w.grid(row=0, column=1)
        # h = tk.Entry(self.frame, width=17, textvariable=self.old_prob)
        # h.grid(row=1, column=1)

        # 3
        w = tk.Label(self.frame, text="Old DS", fg="blue", justify=tk.LEFT)
        w.grid(row=0, column=1)
        h = tk.Entry(self.frame, width=17, textvariable=self.old_DS)
        h.grid(row=1, column=1)
        # 4
        w = tk.Label(self.frame, text="New DS", fg="blue", justify=tk.LEFT)
        w.grid(row=0, column=2)
        h = tk.Entry(self.frame, width=17, textvariable=self.new_DS)
        h.grid(row=1, column=2)
        # 5
        w = tk.Label(self.frame, text="Old CR", fg="blue", justify=tk.LEFT)
        w.grid(row=2, column=0)
        h = tk.Entry(self.frame, width=17, textvariable=self.old_CR)
        h.grid(row=3, column=0)
        # 6
        w = tk.Label(self.frame, text="New CR", fg="blue", justify=tk.LEFT)
        w.grid(row=2, column=1)
        h = tk.Entry(self.frame, width=17, textvariable=self.new_CR)
        h.grid(row=3, column=1)
        # 7
        w = tk.Label(self.frame, text="Old price", fg="blue", justify=tk.LEFT)
        w.grid(row=2, column=2)
        h = tk.Entry(self.frame, width=17, textvariable=self.old_price)
        h.grid(row=3, column=2)

    def _master_frame(self, master=None, **kwargs):
        # Departure port, TYOA-sky
        w = tk.Label(master, text="Departure", fg="blue", justify=tk.LEFT)
        w.grid(row=0, column=0, columnspan=2, padx=10)
        h = tk.Entry(master, width=17, textvariable=self.port_dep)
        h.grid(row=0, column=2, columnspan=2)
        # Destination port: MMY-sky | ISG-sky
        w = tk.Label(master, text="Destination", fg="blue", justify=tk.LEFT)
        w.grid(row=0, column=6, columnspan=2, padx=10)
        h = tk.Entry(master, width=17, textvariable=self.port_des)
        h.grid(row=0, column=8, columnspan=2)
        # Outward day
        w = tk.Label(master, text="Out", fg="green", justify=tk.LEFT)
        w.grid(row=1, column=0)
        h = tk.Entry(master, width=17, textvariable=self.day_out)
        h.grid(row=1, column=2, columnspan=2)
        # Return day - not require
        w = tk.Label(master, text="In", fg="red", justify=tk.LEFT)
        w.grid(row=1, column=6)
        h = tk.Entry(master, width=17, textvariable=self.day_in)
        h.grid(row=1, column=8, columnspan=2)

        # can't use calender because calender module not exist, and idk why.
        # ttkcal = Cal.MyDatePicker(format_str='%02d-%s-%s')
        cal_out = tk.Button(master, text='Date', command=self.make_date_out)
        cal_out.grid(row=1, column=1, sticky='we')

        cal_in = tk.Button(master, text='Date', command=self.make_date_in)
        cal_in.grid(row=1, column=7, sticky='we')

    def make_date_out(self):
        Cal.MyDatePicker(widget=self.day_out, format_str='%s-%02d-%02d')

    def make_date_in(self):
        Cal.MyDatePicker(widget=self.day_in, format_str='%s-%02d-%02d')

    def _ResultFrame(self, master=None, **kwargs):
        rs = tk.Label(master, textvariable=self.result_text, justify=tk.LEFT)
        rs.pack(side=tk.LEFT)

    def clear_log_result(self):
        self.result_text.set('')

    def NewFile(self):
        print "New File!"

    def OpenFile(self):
        name = askopenfilename()
        print name

    def import_transit_prob(self):
        self.import_prob('TRANSIT_PROBABILITY')

    def import_doto(self):
        file = askopenfilename()
        if not file:
            return False
        # print file
        # return False
        with open(file, 'r') as f:
            try:
                data = Yaml.load(f)
                if data['namespace'] and data['namespace'] == 'data_log':
                    self.old_status.set(data['old_status'])
                    self.old_price.set(data['old_price'])
                    self.old_DS.set(data['old_ds'])
                    self.old_CR.set(data['old_cr'])
                    self.new_CR.set(data['new_cr'])
                    self.new_DS.set(data['new_ds'])
                    # self.old_prob.set(data['old_prob'])
                    tkmsg.showinfo('Success', 'Import data success !')
                    return True
                tkmsg.showerror('Error', 'Data not correct the format, please check !')
                return False
            except:
                tkmsg.showerror('Error', 'Please import right format file .yml !')
                return False

    @staticmethod
    def _write_setting():
        dir = askdirectory()
        print dir
        config = ConfigParser.ConfigParser()
        config.read('setting.cfg')
        if config.has_section('PATH'):
            config.set('PATH', 'root_folder', dir)
            # print '- change `root_folder` value -'
            logging.debug('- change `root_folder` value -')
        else:
            config.add_section('PATH')
            config.set('PATH', 'root_folder', dir)
            # print '- section `PATH` is not exist -'
            logging.debug('- section `PATH` is not exist -')
            # print '- Add section `PATH` and set `root_folder` value'
            logging.debug('- Add section `PATH` and set `root_folder` value')
        with open('setting.cfg', 'wb') as configfile:
            config.write(configfile)

    def import_prob(self, section):
        file = askopenfilename()
        if not file:
            return False
        with open(file, 'r') as f:
            try:
                config = Yaml.load(f)
                if not config['namespace'] or config['namespace'] != 'probability':
                    tkmsg.showerror('Error', 'Data not correct the format, please check !')
                    return False
                if section == 'TRANSIT_PROBABILITY':
                    for x in range(0, 9, 1):
                        self.matrix_tp[x].delete(0, tk.END)
                    self.matrix_transit[0][0] = tmp = config[section]['price_up']['price_up']
                    self.matrix_tp[0].insert(0, tmp)
                    self.matrix_transit[0][1] = tmp = config[section]['price_up']['price_keep']
                    self.matrix_tp[1].insert(0, tmp)
                    self.matrix_transit[0][2] = tmp = config[section]['price_up']['price_down']
                    self.matrix_tp[2].insert(0, tmp)
                    self.matrix_transit[1][0] = tmp = config[section]['price_keep']['price_up']
                    self.matrix_tp[3].insert(0, tmp)
                    self.matrix_transit[1][1] = tmp = config[section]['price_keep']['price_keep']
                    self.matrix_tp[4].insert(0, tmp)
                    self.matrix_transit[1][2] = tmp = config[section]['price_keep']['price_down']
                    self.matrix_tp[5].insert(0, tmp)
                    self.matrix_transit[2][0] = tmp = config[section]['price_down']['price_up']
                    self.matrix_tp[6].insert(0, tmp)
                    self.matrix_transit[2][1] = tmp = config[section]['price_down']['price_keep']
                    self.matrix_tp[7].insert(0, tmp)
                    self.matrix_transit[2][2] = tmp = config[section]['price_down']['price_down']
                    self.matrix_tp[8].insert(0, tmp)

                    for x in range(0, 6, 1):
                        self.matrix_ep[x].delete(0, tk.END)
                    self.matrix_emission[0][0] = tmp = config['emission_probability']['price_up']['ds_increase']
                    self.matrix_ep[0].insert(0, tmp)
                    self.matrix_emission[0][1] = tmp = config['emission_probability']['price_up']['ds_decrease']
                    self.matrix_ep[1].insert(0, tmp)
                    self.matrix_emission[1][0] = tmp = config['emission_probability']['price_keep']['ds_increase']
                    self.matrix_ep[2].insert(0, tmp)
                    self.matrix_emission[1][1] = tmp = config['emission_probability']['price_keep']['ds_decrease']
                    self.matrix_ep[3].insert(0, tmp)
                    self.matrix_emission[2][0] = tmp = config['emission_probability']['price_down']['ds_increase']
                    self.matrix_ep[4].insert(0, tmp)
                    self.matrix_emission[2][1] = tmp = config['emission_probability']['price_down']['ds_decrease']
                    self.matrix_ep[5].insert(0, tmp)
                    tkmsg.showinfo('Success', 'Import data success !')
                    return True
            except:
                tkmsg.showerror('Error', 'Please import right format file .yml !')
                return False
        # print self.matrix_transit
        # with open('config.yml', 'w') as configfile:
        #     config.write(configfile)

        print '[-- SET INI FILE COMPLETED --]'

    def About(self):
        tkmsg.showinfo('About', 'Just a simple simulate for auto price')
        print "This is a simple example of a menu"

    def answer(self):
        tkmsg.showerror("Answer", "Sorry, no answer available")

    def callback(sel):
        if tkmsg.askyesno('Verify', 'Really quit?'):
            tkmsg.showwarning('Yes', 'Not yet implemented')
        else:
            tkmsg.showinfo('No', 'Quit has been cancelled')

    # --------------------
    def _read_setting(self):
        config = ConfigParser.ConfigParser()
        data = config.read('setting.cfg')
        # raise error if missing file setting
        if not len(data):
            logging.debug('Missing file `setting.cfg` !')
            self.show_error('Missing File', '`setting.cfg` is missing')
            return False
        if config.has_section('PATH'):
            self.data_roor_folder = config.get('PATH', 'root_folder')
            logging.debug('Get root folder success')
            return True

        return False

    def show_error(self, error_tittle, message):
        tkmsg.showerror(title=error_tittle, message=message)

    def show_info(self, title, message):
        tkmsg.showinfo(title, message)

    def get_live_data(self):
        day = self.day_out.get()
        org = self.port_dep.get() + '-sky'
        des = self.port_des.get() + '-sky'
        # logging.debug('%s_%s' % org, des)
        print des
        if org != 'TYOA-sky':
            logging.debug('- wrong origin_place -')
            self.show_error('Input Data Error', 'Please check input code of `Departure`')
            return False
        if des != 'MMY-sky' and des != 'ISG-sky':
            logging.debug('- wrong destination_place -')
            self.show_error('Input Data Error', 'Please check input code of `Destination`')
            return False
        create_session = rdp.create_session(day=day, org=org, des=des)
        logging.debug('pause for getting session')
        time.sleep(1.2)
        logging.debug('create session complete')
        if create_session['status'] == 0:
            self.show_error('Error', create_session['message'])
            return False
        self.session = create_session['session']
        self.day_in.set(self.session)
        logging.debug(self.session)
        return True
        # json_data = rdp.get_live_data(path=self.data_roor_folder)

    def get_data(self):
        rdp.get_live_data(self.data_roor_folder, self.session, self.day_out.get() )

    def test(self):
        self.calculate_prob()

        if not self.get_live_data():
            self.show_info('Fail', 'Fail on get live data!')
            return False
        # leep a bit after create session
        # time.sleep(1.7)
        file = rdp.get_live_data(self.data_roor_folder, self.session,
                                 self.day_out.get(), self.port_dep.get(), self.port_des.get())
        if not file:
            self.show_error('Get data fail', 'Something wrong was happend, please don\'t smoke. GG !')
            return False
        h = rdp.calculation_price(self.new_DS.get(), self.old_DS.get())
        date = self.day_out.get().replace('-', '')
        path = self.data_roor_folder + '/' + date  # '/20161209'
        # file = path + '/live_price/liveprice_20161021.json'
        status = 0
        if self.new_state == 'Price_up':
            status = 1
        if self.new_state == 'Price_down':
            status = -1
        if status != 0:
            rdp.auto_price(path, file, status, h, self.port_dep.get(), self.port_des.get())
            logging.debug('Auto pricing finish !')
            self.show_info('Success', 'Pricing has been done !')
            return True

