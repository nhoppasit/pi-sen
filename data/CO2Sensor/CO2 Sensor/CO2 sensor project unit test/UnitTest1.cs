using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace CO2_sensor_project_unit_test
{
    [TestClass]
    public class UnitTest1
    {
        byte[] databuf = new byte[20];

        private byte chk_sum()
        {
            byte sum = 0;
            for (int i = 1; i < 8; i++)
            {
                sum += databuf[i];
            }
            byte cal_sum = (byte)(sum & 0xFF);
            cal_sum = (byte)((~cal_sum) + 1);
            return (cal_sum);
        }

        [TestMethod]
        public void TestMethod1()
        {
            databuf = new byte[] { 0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79 };
            var br = chk_sum();
        }
    }
}
