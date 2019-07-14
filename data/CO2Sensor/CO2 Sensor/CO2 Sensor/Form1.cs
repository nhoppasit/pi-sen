using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO.Ports;
using System.IO;
namespace CO2_Sensor
{
    public partial class co2_sensor : Form
    {
        public delegate void InvokeDelegate();
        int co2_state;
        const byte STARTBIT = 0xFF;
        const byte DATABIT  = 2;
        const byte CHECK_VAL = 3;
        int  Highchannel=2, Lowchannel=3;
        byte[] databuf = new byte[20];
        int cnt_data_in = 0;
        int xx=0,xn=0;
        public co2_sensor()
        {
            InitializeComponent();
        }

        private void connect_Click(object sender, EventArgs e)
        {
            if (lisport.Items.Count > 0) // If there are ports available
            {
                serialPort.BaudRate = int.Parse(baud_list.Text);
                serialPort.PortName = lisport.Text;
                if (!serialPort.IsOpen)
                {
                    serialPort.Open();
                    label3.Text = "Connect";
                }
            }

        }

        private void discon_Click(object sender, EventArgs e)
        {
            if (serialPort.IsOpen)
            {
                serialPort.Close(); // Close port
                label3.Text = "Disconnect";
            }
        }

        private void serialPort_DataReceived(object sender, System.IO.Ports.SerialDataReceivedEventArgs e)
        {
            textBox2.BeginInvoke(new InvokeDelegate(updateTextbox));
        }
        private void updateTextbox()
        {
            int inputByte = serialPort.BytesToRead;
            byte[] bytes = new byte[inputByte];
            serialPort.Read(bytes, 0, inputByte);
            for (int i = 0; i < inputByte; i++)
            {
                databuf[cnt_data_in] = bytes[i];
                cnt_data_in++;
            }
            if (cnt_data_in > 8)
            {
                process_data();
                cnt_data_in = 0;
            }
        }
        private void process_data()
        {
            if (chk_sum() == databuf[8])
            { 
                //Gas Concentration = High channel*256+low channel, No.of sensor: 0x01
                int ppm = databuf[Highchannel] * 256 + databuf[Lowchannel];
                int temp = databuf[4];
                temp = temp - 40;
                textBox1.Text = temp.ToString();
                textBox2.Text = ppm.ToString();
                update_grapg(ppm);
            }
        }
        private int chk_sum()
        {
            byte sum = 0;
            for (int i = 1; i < 8; i++)
            {
                sum += databuf[i];
            }
            //byte cal_sum = (byte)(sum & 0xFF);
            //cal_sum = (byte)((~cal_sum) + 1);
            int cal_sum = (sum & 0xFF);
            cal_sum = ((~cal_sum) + 1) & 0xFF;
            return (cal_sum);
        }
        void update_grapg(int gas)
        {
            chart1.Series["PPM"].Points.AddY(gas);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            xx = 0;
            timer1.Enabled=true;
        }

        private void co2_sensor_Load(object sender, EventArgs e)
        {
            string[] s = SerialPort.GetPortNames();
            int i = 0;

            baud_list.Items.Clear();
            baud_list.Items.Add("1200");
            baud_list.Items.Add("2400");
            baud_list.Items.Add("4800");
            baud_list.Items.Add("9600");
            baud_list.Items.Add("19200");
            baud_list.Items.Add("38400");
            baud_list.Items.Add("57600");
            baud_list.Items.Add("115200");
            baud_list.Items.Add("230400");
            baud_list.SelectedIndex = 3;
            if (s.Length > 0)
            {
                lisport.Items.Clear();
                foreach (string port in s)
                {
                    lisport.Items.Add(s[i]);
                    i++;
                }
                lisport.SelectedIndex = 0;

            }
            else
            {
                MessageBox.Show("Serial port not found");
                button1.Enabled = false;
                button2.Enabled = false;
                connect.Enabled = false;
                discon.Enabled = false;
            }

        }

        private void button2_Click(object sender, EventArgs e)
        {
            timer1.Enabled = false;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            byte[] data = { 0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79 };
            serialPort.Write(data, 0, 9);
        
        }

        
    }
}
