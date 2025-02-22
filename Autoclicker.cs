using System;
using System.Threading;
using System.Windows.Forms;
using WindowsInput;
using WindowsInput.Native;

public class AutoClicker
{
    private Thread clickThread;
    private bool clicking = false;
    private int minCPS = 14, maxCPS = 14;
    private VirtualKeyCode toggleKey = VirtualKeyCode.F6;
    private readonly InputSimulator inputSimulator = new InputSimulator();

    public bool Clicking => clicking;

    public int MinCPS { get => minCPS; set => minCPS = value; }
    public int MaxCPS { get => maxCPS; set => maxCPS = value; }
    public VirtualKeyCode ToggleKey { get => toggleKey; set => toggleKey = value; }

    public void Start()
    {
        clickThread = new Thread(ClickLoop) { IsBackground = true };
        clickThread.Start();
    }

    public void ToggleClicking()
    {
        clicking = !clicking;
        Console.WriteLine($"Clicking toggled to: {(clicking ? "ON" : "OFF")}");
    }

    private void ClickLoop()
    {
        while (true)
        {
            if (clicking)
            {
                Random rnd = new Random();
                int delay = 1000 / rnd.Next(minCPS, maxCPS + 1);
                inputSimulator.Mouse.LeftButtonClick();
                Thread.Sleep(delay);
            }
            else
            {
                Thread.Sleep(100);
            }
        }
    }
}

