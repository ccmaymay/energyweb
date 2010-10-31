//joseph king june 2, 2008
//revised oct 4, 2008
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
 	Socket[] sender = new Socket[100];
	double 		 		awatthr, bwatthr, cwatthr, avarhr, bvarhr, cvarhr, avahr, bvahr, cvahr;
	double				airms, birms, cirms, avrms, bvrms, cvrms, temp, freq;
	Byte				rindex;		
	float factor = 6;     
 
//	try{
 
//connect to sql, create db, create table, write a line to table--note that we log in we must choose an existing database

	SqlConnection thisConnection = new SqlConnection("server=(local)\\SQLEXPRESS;Trusted_Connection=yes;database=Northwind;Integrated Security=SSPI");
        thisConnection.Open();
//	SqlCommand  createDb = new SqlCommand("CREATE DATABASE East3Db", thisConnection);
//	createDb.ExecuteNonQuery();
        thisConnection.ChangeDatabase("East3Db");
//	SqlCommand  createTable = new SqlCommand( "CREATE TABLE MainTable (COL1 datetime, COL2 tinyint, COL3 float, COL4 float, COL5 float, COL6 float, COL7 float, COL8 float,COL9 float, COL10 float, COL11 float, COL12 float, COL13 float, COL14 float,COL15 float, COL16 float, COL17 float, COL18 float, COL19 float)", thisConnection);
//	createTable.ExecuteNonQuery();
 
//Connect to a remote device.
//define endpoint for Case
        IPHostEntry ipHostInfo = Dns.GetHostByName("172.31.10.73");
        IPAddress ipAddress = ipHostInfo.AddressList[0];
        IPEndPoint remoteEP = new IPEndPoint(ipAddress,4001);

	int xx = 1; // increment for the socket

// Create a TCP/IP  socket.

        sender[xx] = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp );

// Connect the socket to the remote endpoint
 
        sender[xx].Connect(remoteEP);
        Console.WriteLine("Socket connected to {0}",sender[xx].RemoteEndPoint.ToString());

	while(xx>0){ //trap in a loop
		int index = 0;
		while(index<45)
			{
                	int bytesRec = sender[xx].Receive(bytes,index, 45, SocketFlags.None);
			index = index+bytesRec;
			}

	if (  (bytes[0] != 0x52 ) || (bytes[1] != 0x54) || (bytes[2] != 0x53) || (bytes[3] != 0x44)  )          
              	{Console.WriteLine("Bad Data! Printing Data and Closing Socket");
		// Print data to console
      			for(Int32 i=0;i< 45;i++)
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
      			for(Int32 i=0;i< 45;i++)//output results to console
			{
			Console.Write(" {0:x2}",bytes[i]);
			}
			Console.WriteLine("Begin new line.");
			Console.WriteLine(xx);
			//Console.WriteLine(Encoding.ASCII.GetChars(bytes));  //writes the gibberish

	//output results to database
	rindex = bytes[4];
	awatthr = factor * (  ( (long)bytes[5]<<8 )|( (uint)bytes[6])  );
	bwatthr = factor * (  ( (long)bytes[7]<<8 )|( (uint)bytes[8])  );
	cwatthr = factor * (  ( (long)bytes[9]<<8 )|( (uint)bytes[10])  );
	avarhr = factor * (  ( (long)bytes[11]<<8 )|( (uint)bytes[12])  );
	bvarhr = factor * (  ( (long)bytes[13]<<8 )|( (uint)bytes[14])  );
	cvarhr = factor * (  ( (long)bytes[15]<<8 )|( (uint)bytes[16])  );
	avahr = factor * (  ( (long)bytes[17]<<8 )|( (uint)bytes[18])  );
	bvahr = factor * (  ( (long)bytes[19]<<8 )|( (uint)bytes[20])  );
	cvahr = factor * (  ( (long)bytes[21]<<8 )|( (uint)bytes[22])  );
	airms = factor * (  ( (long)bytes[23]<<16 )|( (uint)bytes[24]<<8)|( (uint)bytes[25]) );
	birms = factor * (  ( (long)bytes[26]<<16 )|( (uint)bytes[27]<<8)|( (uint)bytes[28]) );
	cirms = factor * (  ( (long)bytes[29]<<16 )|( (uint)bytes[30]<<8)|( (uint)bytes[31]) );
	avrms =  (  ( (long)bytes[32]<<16 )|( (uint)bytes[33]<<8)|( (uint)bytes[34]) );
	bvrms =  (  ( (long)bytes[35]<<16 )|( (uint)bytes[36]<<8)|( (uint)bytes[37]) );
	cvrms =  (  ( (long)bytes[38]<<16 )|( (uint)bytes[39]<<8)|( (uint)bytes[40]) );
	freq = ( (  ( (long)bytes[41]<<8 )|( (uint)bytes[42])  )  >> 4 );
	temp = 25 +   (bytes[43] - 0xdf ) * 3 ;//  at Amb = 25C, register = DF = Offset

	SqlCommand insertData = new SqlCommand( "INSERT INTO MainTable (COL1, COL2, COL3, COL4, COL5, COL6, COL7, COL8, COL9, COL10, COL11, COL12, COL13, COL14, COL15, COL16, COL17, COL18, COL19) VALUES (GetDate(), "+rindex+", "+awatthr+", "+bwatthr+", "+cwatthr+", "+avarhr+", "+bvarhr+", "+cvarhr+", "+avahr+", "+bvahr+", "+cvahr+", "+airms+", "+birms+", "+cirms+", "+avrms+", "+bvrms+", "+cvrms+", "+freq+", "+temp+")", thisConnection);
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

}// end of class


