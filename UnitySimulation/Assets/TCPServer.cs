using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class TCPServer : MonoBehaviour
{
    public CommandProcessor commandProcessor;

    private TcpListener tcpListener;
    private Thread tcpListenerThread;
    private TcpClient connectedTcpClient;
    private static readonly Queue<Action> executeOnMainThreadQueue = new Queue<Action>();

    // Start is called before the first frame update
    void Start()
    {
        tcpListenerThread = new Thread(new ThreadStart(ListenForRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }

    private void ListenForRequests()
    {
        try
        {
            tcpListener = new TcpListener(System.Net.IPAddress.Any, 8052);
            tcpListener.Start();
            Debug.Log("Server is listening");

            while (true)
            {
                TcpClient client = tcpListener.AcceptTcpClient();
                Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient));
                clientThread.Start(client);
            }
        }
        catch (ThreadAbortException)
        {
            Debug.Log("Thread was aborted");
        }
        catch (Exception e)
        {
            Debug.LogError($"An exception occurred: {e.Message}");
        }
    }

    private void HandleClient(object obj)
    {
        TcpClient client = (TcpClient)obj;
        NetworkStream stream = client.GetStream();
        byte[] bytes = new byte[1024];

        try
        {
            while (true)
            {
                int length = stream.Read(bytes, 0, bytes.Length);
                if (length == 0) break; // Check for disconnection

                string clientMessage = Encoding.ASCII.GetString(bytes, 0, length);
                Debug.Log($"Received: {clientMessage}");

                lock (executeOnMainThreadQueue)
                {
                    executeOnMainThreadQueue.Enqueue(() => commandProcessor.ProcessCommand(clientMessage));
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"Error in HandleClient: {e.Message}");
        }
        finally
        {
            stream.Close();
            client.Close();
        }
    }

    void Update()
    {
        while (executeOnMainThreadQueue.Count > 0)
        {
            Action action = null;
            lock (executeOnMainThreadQueue)
            {
                if (executeOnMainThreadQueue.Count > 0)
                {
                    action = executeOnMainThreadQueue.Dequeue();
                }
            }
            action?.Invoke();
        }
    }

    void OnApplicationQuit()
    {
        tcpListener?.Stop();
        if (tcpListenerThread != null)
        {
            // Safely stop the thread
            tcpListenerThread.Abort();
            tcpListenerThread.Join();
        }
    }
}
