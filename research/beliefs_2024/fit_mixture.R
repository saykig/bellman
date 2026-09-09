# Existing stratEst estimator; source-only table is prepared by the Python runner.
# Arguments: source CSV, output directory, catalogue (ten or six).
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==3)
library(stratEst)
stopifnot(as.character(packageVersion('stratEst'))=='1.1.8')
x <- read.csv(args[1])
stopifnot(all(x$treatment==2), all(x$session %in% c(1,2,3,4,10,11,14,15)),
          all(x$supergame>=5), all(x$round>=1 & x$round<=8))
x$subject <- as.integer(factor(paste(x$session,x$id,sep=':')))
x$choice <- ifelse(x$coop==1,'c','d')
x$other <- ifelse(x$o_coop==1,'c','d')
data <- stratEst.data(x,choice='choice',input=c('choice','other'),input.lag=1,
                      id='subject',game='supergame',period='round')
threshold <- function(k) {
  outputs <- c(rep(1,k-1),0)
  transitions <- cbind(pmin(seq_len(k)+1,k),rep(k,k),rep(k,k),rep(k,k))
  stratEst.strategy(choices=c('d','c'),inputs=c('cc','cd','dc','dd'),
    prob.choices=as.vector(rbind(1-outputs,outputs)),
    tr.inputs=as.vector(t(transitions)),num.states=as.numeric(k))
}
strategies <- list(AD=strategies.PD$ALLD,AC=strategies.PD$ALLC,
  GRIM=strategies.PD$GRIM,TFT=strategies.PD$TFT,STFT=strategies.PD$DTFT,
  T8=threshold(8),T7=threshold(7),T6=threshold(6),
  GRIM2=strategies.PD$GRIM2,TF2T=strategies.PD$TF2T)
if(args[3]=='six') strategies <- strategies[c('AD','AC','GRIM','TFT','GRIM2','TF2T')]
stopifnot(args[3] %in% c('ten','six'))
dir.create(args[2],recursive=TRUE,showWarnings=FALSE)
for(n in names(strategies)) write.csv(strategies[[n]],file.path(args[2],paste0('automaton-',n,'.csv')),row.names=FALSE)
set.seed(20260909)
fit <- stratEst.model(data,strategies,response='pure',r.trembles='global',select=NULL,
  outer.runs=20,inner.runs=10,outer.max=2000,inner.max=20,outer.tol=1e-10,verbose=FALSE)
# Do not retain post.assignments or original rows. Only aggregate fitted objects.
write.csv(fit$shares,file.path(args[2],'shares.csv'),row.names=TRUE)
write.csv(fit$trembles,file.path(args[2],'trembles.csv'),row.names=TRUE)
capture.output(str(fit[c('shares','trembles','loglike','num.ids','num.obs','eval','tol.val','convergence')]),
               file=file.path(args[2],'diagnostics.txt'))
dput(fit[c('loglike','num.ids','num.obs','eval','tol.val','convergence')],
     file=file.path(args[2],'diagnostics.R'))
writeLines(capture.output(sessionInfo()),file.path(args[2],'runtime.txt'))
