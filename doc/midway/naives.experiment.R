
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
recall = c(0.477342995169, 0.531787439614, 0.590048309179, 0.607004830918, 0.65922705314, 0.681304347826, 0.715)
precision = c(0.529710144928, 0.532463768116, 0.520531400966, 0.495859213251, 0.488949275362, 0.478904991948, 0.458405797101)
fscore = c(0.529710144928, 0.532463768116, 0.520531400966, 0.495859213251, 0.488949275362, 0.478904991948, 0.458405797101)

# Calculate range from 0 to max value of cars and trucks
g <- range <- range(0, recall, precision)

# Graph autos using y axis that ranges from 0 to max 
# value in cars or trucks vector.  Turn off axes and 
# annotations (axis labels) so we can specify them ourself
plot(x=seq(4, 10), y=recall, type="o", col="blue", ylim=c(0.45, 0.75), xlab="# of Top N Tags")


# Create box around plot
box()

# Graph trucks with red dashed line and square points
lines(precision, type="o", pch=22, lty=2, col="red")

# Create a title with a red, bold/italic font
title(main="Recall, Precision and F-measure", col.main="red", font.main=4)

# Create a legend at (1, g <- range[2]) that is slightly smaller 
# (cex) and uses the same line colors and points used by 
# the actual plots 
legend(1, g <- range[2], c("Recall","Precision"), cex=0.8, 
          col=c("blue","red"), pch=21:22, lty=1:2);
dev.off()
