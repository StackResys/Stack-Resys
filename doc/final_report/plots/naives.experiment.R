
#x = seq(4, 10)
#
#grange <- range(0, recall, precision)
#plot(x, recall, type="o", col="blue", ylim = c(0.4, 0.8), xlab="Number of Top N Tags", axes=FALSE, ann=FALSE)
#lines(x, precision, type="o", col="red", lty=2)
#title(main="Precision and Recall")
#
#legend(1, grange[2], c("Recall", "Precision"), cex=0.8, col=c("blue", "red"), pch=21:22, lty=1:2)


png("naives.png")
# Define 2 vectors
kl_prec = c(0.480556,0.426503,0.383751,0.348973,0.322981,0.302737)
kl_recall = c(0.447986,0.455099,0.494108,0.535115,0.568587,0.594717)

# Calculate range from 0 to max value of cars and trucks
grange <- range(0, kl_recall, kl_prec)

# Graph autos using y axis that ranges from 0 to max 
# value in cars or trucks vector.  Turn off axes and 
# annotations (axis labels) so we can specify them ourself
plot(x=seq(4,10), y=kl_recall, type="o", col="blue", ylim=c(0.45, 0.75), xlab="# of Top N Tags")


# Create box around plot
box()

# Graph trucks with red dashed line and square points
lines(x=seq(4, 10), kl_prec, type="o", pch=22, lty=2, col="red")

# Create a title with a red, bold/italic font
title(main="Recall and Precision", col.main="red", font.main=4)

# Create a legend at (1, g <- range[2]) that is slightly smaller 
# (cex) and uses the same line colors and points used by 
# the actual plots 
print(grange[2])
legend(4, grange[2], c("Recall","Precision"), cex=0.8, 
          col=c("blue","red"), pch=21:22, lty=1:2);
dev.off()
