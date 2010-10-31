//joseph king august20, 2008
//revised nov 4, 2008
//all rights reserved
//program creates database/table creates socket/opens socket;

using System;
using System.Data;
using System.Data.SqlClient;
using System.Net;
using System.Net.Sockets;
using System.Text;

class OpenandFill{

static void Main() {

       	byte[] bytes = new byte[1024];	// Data buffer for incoming data
	Socket[] sender = new Socket[1000000];
	Byte				rindex, srcep;		
	int				panid, srcaddr, uwatts;
	uint				rfdtimedata;
	float 		 		watts;
	float factor = 1; 

//connect to sql, create db, create table, write a line to table--note that we log in we must choose an existing database


	SqlConnection thisConnection = new SqlConnection("server=(local)\\SQLEXPRESS;Trusted_Connection=yes;database=Northwind;Integrated Security=SSPI");
           	thisConnection.Open();
	 //SqlCommand  createDb = new SqlCommand("CREATE DATABASE StudentshopDb", thisConnection);
	 //createDb.ExecuteNonQuery();
            	thisConnection.ChangeDatabase("StudentshopDb");
	// SqlCommand  createTable = new SqlCommand( "CREATE TABLE MainTable (COL1 datetime, COL2 int, COL3 int, COL4 tinyint, COL5 tinyint, COL6 bigint, COL7 float)", thisConnection);
	// createTable.ExecuteNonQuery();

	// Connect to a remote device.
	//define endpoint
            	 IPHostEntry ipHostInfo = Dns.GetHostEntry("134.173.38.20");
                 IPAddress ipAddress = ipHostInfo.AddressList[0];
           	 IPEndPoint remoteEP = new IPEndPoint(ipAddress,4001);

	int xx = 1; // increment for the socket

	// Create a TCP/IP  socket.

        sender[xx] = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp );

	// Connect the socket to the remote endpoint. Catch any errors.

        sender[xx].Connect(remoteEP);
        Console.WriteLine("Socket connected to {0}",sender[xx].RemoteEndPoint.ToString());

	while(xx>0){ //trap in a loop

		int index = 0;
		while(index<19)
			{
                	int bytesRec = sender[xx].Receive(bytes,index, 19, SocketFlags.None);
			index = index+bytesRec;	
			}
	if (  (bytes[0] != 0x52 ) || (bytes[1] != 0x53)  )          
              	{Console.WriteLine("Bad Data! Printing Data and Closing Socket");
		// Print data to console
      			for(Int32 i=0;i< 19;i++)
			{
			Console.Write(" {0:x2}",bytes[i]);
			}
			Console.WriteLine("Begin new line.");
		//Console.WriteLine(Encoding.ASCII.GetChars(bytes));  //writes the gibberish
		// Closing socket
              	sender[xx].Shutdown(SocketShutdown.Both);
             	sender[xx].Close();
		xx = xx + 1;
		//Reopen socket
		// Create a TCP/IP  socket.
            	sender[xx] = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp );
		// Connect the socket to the remote endpoint.  
              	sender[xx].Connect(remoteEP);
              	Console.WriteLine("Socket connected to {0}",sender[xx].RemoteEndPoint.ToString());
		}

		else
		{

      	for(Int32 i=0;i< 19;i++) //output results to console
	{
	Console.Write(" {0:x2}",bytes[i]);
	}
	Console.WriteLine("New line."); 
	Console.WriteLine(xx);

//output results to database
//bytes 0 & 1 are the R & S
	panid =  (int)((bytes[2]<<8)|bytes[3]);
	srcaddr = (int)( (bytes[4]<<8)|bytes[5] );
	rindex = bytes[6];
	srcep = bytes[7];
	rfdtimedata = (uint)( (bytes[8]<<24)|(bytes[9]<<16)|(bytes[10]<<8)|bytes[11] );
//bytes[12] is the number of data bytes = 4
	uwatts =   ( (bytes[16]<<24)|(bytes[15]<<16)|(bytes[14]<<8)|bytes[13] );
	unsafe {
		watts = *(float*)&uwatts; 				//converts to a float
		}
	if (watts<1)
		{
		watts=0;
		}	
	SqlCommand insertData = new SqlCommand("INSERT INTO MainTable (COL1, COL2, COL3, COL4, COL5, COL6, COL7) VALUES (GetDate(), "+panid+", "+srcaddr+", "+rindex+", "+srcep+", "+rfdtimedata+", "+watts+")", thisConnection);
	insertData.ExecuteNonQuery();

	}//end of else

	}//trapped while loop

	//close database connection
            	thisConnection.Close();
            	Console.WriteLine("Database Connection Closed.");

	// Release the socket.
              Console.WriteLine("Closing Socket");
              sender[xx].Shutdown(SocketShutdown.Both);
              sender[xx].Close();
    }//end of main

}//end of class



    


