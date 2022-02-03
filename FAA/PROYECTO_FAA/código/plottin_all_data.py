import numpy as np
## Plotting all data

def plotting_data(ax, bData, wData, idx_Data_dst, y_lim, y_ticks, color_prim=(0.3,0.3,0.3), color_sec=(1.0,0.5,0.1), line_width=1.5):
   
   # primero platano y luego vino
   for i, idx_Data in zip(range(0, 6), idx_Data_dst):
      if i <= 1:
         # banana
         ax[i,0].plot(bData[:, 0], bData[:, idx_Data[0]], color=color_prim, lw=line_width )
         #ax[i,0].set_ylim(y_lim[i][0], y_lim[i][1])
         ax[i,0].set_yticks(y_ticks[i])
         # vino
         ax[i,1].plot(wData[:, 0], wData[:, idx_Data[0]], color=color_prim, lw=line_width)
         #ax[i,1].set_ylim(y_lim[i][0], y_lim[i][1])
         ax[i,1].set_yticks(y_ticks[i])
      else:
         # banana
         ax[i,0].plot(bData[:, 0], bData[:, idx_Data[i][0]], color=color_prim, lw=line_width)
         ax[i,0].plot(bData[:, 0], bData[:, idx_Data[i][1]], '-', color=color_sec, lw=line_width)
         #ax[i,0].set_ylim(y_lim_0[0], y_lim_0[1])
         ax[i,0].set_yticks(y_ticks[i])
         # vino
         ax[i,1].plot( wData[:,0], wData[:, idx_Data[i][0]], color=color_prim, lw=line_width, label=r"$R_"+ idx_Data[i][0] +"$"  )
         ax[i,1].plot( wData[:,0], wData[:, idx_Data[i][1]], color=color_sec, lw=line_width, label=r"$R_"+ idx_Data[i][1] +"$"  )
         #ax[i,1].set_ylim(y_lim_0[0], y_lim_0[1])
         ax[i,1].set_yticks(y_ticks[i])

         ax[i,1].legend(frameon=False, fontsize=12, bbox_to_anchor=(-0.08,0.9), handletextpad=0)

   return


# 0, 1, 2, 3, 4, 5
idx_Data_dst = [[10], [9], [1, 4], [2, 3], [5, 6], [7, 8]]
# colores serie 0 y 1
color_green = (0.1,0.8,0.1)
color_red = (1.0,0.1,0.0)
# colores serie 2, 3, 4 y 5
color_prim = (0.3,0.3,0.3)
color_sec = (1.0,0.5,0.1)

line_width = 1.5

# y_lim_0 = [55, 65.4]
# y_lim_1 = [26.1, 29.9]
# y_lim_2 = [7.2, 13.9]
# y_lim_3 = [3.2, 12.9]
# y_lim_4 = [3.0, 15]
# y_lim_5 = [1.1, 6.8]
y_lim = [[55, 65.4], [26.1, 29.9], [7.2, 13.9], [3.2, 12.9], [3.0, 15], [1.1, 6.8]]
#y_ticks_0 = np.arange(56., 65.5, 3)
#y_ticks_1 = np.arange(27., 29.5, 1)
#y_ticks_2 = np.arange(8., 12.5, 2)
#y_ticks_3 = np.arange(5., 12.5, 2)
#y_ticks_4 = np.arange(4., 12.5, 4)
#y_ticks_5 = np.arange(2., 6.5, 2)
ticks_val1 = [56., 27., 8., 5., 4., 2.]
ticks_val2 = [65.5, 29.5, 12.5, 12.5, 12.5, 6.5]
ticks_val3 = [3, 1, 2, 2, 4, 2]
y_ticks = [np.arange(val1, val2, val3) for val1, val2, val3 in zip(ticks_val1, ticks_val2, ticks_val3) ]

# primero platano y luego vino
for i, idx_Data in zip(range(0, 6), idx_Data_dst):
   if i <= 1:
      # banana
      ax[i,0].plot(bData[:, 0], bData[:, idx_Data[0]], color=color_prim, lw=line_width )
      #ax[i,0].set_ylim(y_lim[i][0], y_lim[i][1])
      ax[i,0].set_yticks(y_ticks[i])
      # vino
      ax[i,1].plot(wData[:, 0], wData[:, idx_Data[0]], color=color_prim, lw=line_width)
      #ax[i,1].set_ylim(y_lim[i][0], y_lim[i][1])
      ax[i,1].set_yticks(y_ticks[i])
   else:
      # banana
      ax[i,0].plot(bData[:, 0], bData[:, idx_Data[i][0]], color=color_prim, lw=line_width)
      ax[i,0].plot(bData[:, 0], bData[:, idx_Data[i][1]], '-', color=color_sec, lw=line_width)
      #ax[i,0].set_ylim(y_lim_0[0], y_lim_0[1])
      ax[i,0].set_yticks(y_ticks[i])
      # vino
      ax[i,1].plot( wData[:,0], wData[:, idx_Data[i][0]], color=color_prim, lw=line_width, label=r"$R_"+ idx_Data[i][0] +"$"  )
      ax[i,1].plot( wData[:,0], wData[:, idx_Data[i][1]], color=color_sec, lw=line_width, label=r"$R_"+ idx_Data[i][1] +"$"  )
      #ax[i,1].set_ylim(y_lim_0[0], y_lim_0[1])
      ax[i,1].set_yticks(y_ticks[i])

      ax[i,1].legend(frameon=False, fontsize=12, bbox_to_anchor=(-0.08,0.9), handletextpad=0)
